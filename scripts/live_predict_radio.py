# live_predict.py

import sys
import os
import numpy as np
import pandas as pd
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from d3rlpy.dataset import MDPDataset

# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Expect: id patient_name age tumor_size grade er pr her2
if len(sys.argv) != 9:
    print("ERROR: expected 8 arguments: id patient_name age tumor_size grade er pr her2")
    sys.exit(1)

# Capture ID and Patient Name (not used for model input)
patient_id = str(sys.argv[1])
patient_name = sys.argv[2]

age = float(sys.argv[3])
tumor_size = float(sys.argv[4])
grade = int(sys.argv[5])
er = int(sys.argv[6])
pr = int(sys.argv[7])
her2 = int(sys.argv[8])

# Exclude id and patient_name from model state
state = np.array([[age, tumor_size, grade, er, pr, her2]], dtype=np.float32)

config = DiscreteCQLConfig()
cql = DiscreteCQL(config=config, device="cpu", enable_ddp=False)

dummy_obs = np.array([[age, tumor_size, grade, er, pr, her2]], dtype=np.float32)
dummy_act = np.array([0, 1], dtype=np.int64)
dummy_rew = np.zeros(2, dtype=np.float32)
dummy_term = np.ones(2, dtype=bool)
dummy_dataset = MDPDataset(
    np.vstack([dummy_obs, dummy_obs]),
    dummy_act,
    dummy_rew,
    dummy_term
)
cql.build_with_dataset(dummy_dataset)

model_path = os.path.join(SCRIPT_DIR, "..", "model", "radio_cql_brca_metabric_model.pt")
cql.load_model(model_path)

action = int(cql.predict(state)[0])
msg = "Recommend Radio Therapy" if action == 1 else "Avoid Radio Therapy"

# Print only the message without action number
print(f"Prediction: {msg}")

# Optional logging (now includes ID and Patient Name)
log_path = os.path.join(SCRIPT_DIR, "..", "data", "live_predictions_radio_log.csv")
os.makedirs(os.path.dirname(log_path), exist_ok=True)
new_row = pd.DataFrame([{
    "ID": patient_id,
    "Patient Name": patient_name,
    "Age": age,
    "Tumor Size": tumor_size,
    "Grade": grade,
    "ER": er,
    "PR": pr,
    "HER2": her2,
    "Predicted Action": msg
}])
# Append without header if file exists
header = not os.path.exists(log_path)
new_row.to_csv(log_path, mode="a", index=False, header=header)
