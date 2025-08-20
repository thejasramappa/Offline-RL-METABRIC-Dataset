# predict_treatment.py

import pandas as pd
import numpy as np
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from d3rlpy.dataset import MDPDataset

# === Step 1: Load Sample Patient Data ===
df = pd.read_csv("../data/cleaned_metabric_hormone.csv")

# Define the same state columns used during training
state_cols = ['Age at Diagnosis', 'Tumor Size', 'Neoplasm Histologic Grade',
              'ER Status', 'PR Status', 'HER2 Status']

# Select the first 5 patients as sample input
sample_patients = df[state_cols].iloc[15:45]
sample_array = sample_patients.values.astype(np.float32)

print("📋 Sample Patient Profiles:")
print(sample_patients)

# === Step 2: Load Trained CQL Model ===
config = DiscreteCQLConfig()
cql = DiscreteCQL(config=config, device="cpu", enable_ddp=False)

# Build with a dummy MDPDataset to initialize model shapes
dummy_obs = sample_array
# Alternate between 0 and 1 to ensure both actions are present
dummy_act = np.array([0, 1] * (dummy_obs.shape[0] // 2 + 1))[:dummy_obs.shape[0]]
dummy_rew = np.zeros(dummy_obs.shape[0], dtype=np.float32)
dummy_term = np.ones(dummy_obs.shape[0], dtype=bool)

dummy_dataset = MDPDataset(dummy_obs, dummy_act, dummy_rew, dummy_term)
cql.build_with_dataset(dummy_dataset)

cql.load_model("../model/hormone_cql_brca_metabric_model.pt")  # adjust path if needed

# === Step 3: Predict Treatment Actions ===
predicted_actions = cql.predict(sample_array)

print("\n🤖 Predicted HormoneTherapy Recommendations:")
for idx, action in enumerate(predicted_actions):
    result = "✅ Recommend HormoneTherapy" if action == 1 else "❌ Avoid HormoneTherapy"
    print(f"Patient {idx + 1}: Action = {action} → {result}")
