import sys
import os
import numpy as np
import torch
import pandas as pd
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from d3rlpy.dataset import MDPDataset

# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main():
    # Expect: id patient_name age tumor_size grade er pr her2
    if len(sys.argv) != 9:
        print("ERROR: expected 8 arguments: id patient_name age tumor_size grade er pr her2")
        sys.exit(1)

    # New: capture id and patient_name (not used for model input)
    patient_id = str(sys.argv[1])
    patient_name = sys.argv[2]

    age = float(sys.argv[3])
    tumor_size = float(sys.argv[4])
    histologic_grade = int(sys.argv[5])
    er_status = int(sys.argv[6])
    pr_status = int(sys.argv[7])
    her2_status = int(sys.argv[8])

    # Path to trained model (.d3 is a binary checkpoint)
    model_path = os.path.join(SCRIPT_DIR, "..", "model", "all_cql_brca_metabric_model.d3")

    # Instantiate DiscreteCQL (matching training)
    config = DiscreteCQLConfig()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    enable_ddp = False
    cql = DiscreteCQL(config, device, enable_ddp)

    # Build network with correct shapes: obs_dim=6, num_actions=8
    obs_dim = 6
    num_actions = 8
    dummy_obs = np.zeros((num_actions, obs_dim), dtype=np.float32)
    dummy_act = np.arange(num_actions, dtype=np.int64).reshape(-1, 1)  # actions 0..7
    dummy_rew = np.zeros(num_actions, dtype=np.float32)
    dummy_term = np.ones(num_actions, dtype=bool)
    dummy_ds = MDPDataset(dummy_obs, dummy_act, dummy_rew, dummy_term)
    cql.build_with_dataset(dummy_ds)

    # Now load weights
    cql.load_model(model_path)

    # Prepare state (exclude id and patient_name)
    patient_features = np.array(
        [[age, tumor_size, histologic_grade, er_status, pr_status, her2_status]],
        dtype=np.float32,
    )

    # Predict discrete action id (0..7)
    pred_action = int(cql.predict(patient_features)[0])

    # Map 0..7 to treatment combinations used in training
    labels = {
        0: "none",
        1: "chemotherapy",
        2: "radio_therapy",
        3: "chemotherapy+radio_therapy",
        4: "hormone_therapy",
        5: "chemotherapy+hormone_therapy",
        6: "radio_therapy+hormone_therapy",
        7: "chemotherapy+radio_therapy+hormone_therapy",
    }

    # Produce a single line for Flask to parse: "Prediction: <message>"
    pretty = {
        0: "No Treatment",
        1: "Chemotherapy",
        2: "Radiotherapy",
        3: "Chemotherapy and Radiotherapy",
        4: "Hormone Therapy",
        5: "Chemotherapy and Hormone Therapy",
        6: "Radiotherapy and Hormone Therapy",
        7: "Chemotherapy, Radiotherapy and Hormone Therapy",
    }
    result_text = pretty.get(pred_action, 'Unknown')
    print(f"Prediction: {result_text}")

    # Log the prediction result (now includes ID and Patient Name)
    log_path = os.path.join(BASE_DIR, "..", "data", "live_predict_all_log.csv")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    cols = ["ID", "Patient Name", "Age", "Tumor Size", "Grade", "ER", "PR", "HER2", "Predicted Action"]
    row = [[
        patient_id,
        patient_name,
        age,
        tumor_size,
        histologic_grade,
        er_status,
        pr_status,
        her2_status,
        result_text
    ]]

    header = not os.path.exists(log_path) or os.path.getsize(log_path) == 0
    pd.DataFrame(row, columns=cols).to_csv(log_path, mode="a", index=False, header=header, encoding="utf-8")

if __name__ == "__main__":
    main()
