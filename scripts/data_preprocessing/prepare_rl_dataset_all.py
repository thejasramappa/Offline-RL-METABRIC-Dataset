import pandas as pd
import numpy as np
import pickle
from d3rlpy.dataset import MDPDataset

# Load dataset
df = pd.read_csv("../../data/cleaned_metabric_all_treatment.csv")

# Standardize column names
df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
print("✅ Columns in dataset:", df.columns.tolist())

# Define state features
state_features = [
    "age_at_diagnosis",
    "tumor_size",
    "neoplasm_histologic_grade",
    "er_status",
    "pr_status",
    "her2_status",
]

# Build treatment combinations from binary flags
def get_treatment_combo(row):
    combo = []
    if row["chemotherapy"] == 1:
        combo.append("chemo")
    if row["radio_therapy"] == 1:
        combo.append("radio")
    if row["hormone_therapy"] == 1:
        combo.append("hormone")
    return "+".join(combo) if combo else "none"

# Action mapping
treatment_mapping = {
    "none": 0,
    "chemo": 1,
    "radio": 2,
    "hormone": 3,
    "chemo+radio": 4,
    "chemo+hormone": 5,
    "radio+hormone": 6,
    "chemo+radio+hormone": 7,
}

observations, actions, rewards, terminals = [], [], [], []

for idx, row in df.iterrows():
    # State vector
    state = row[state_features].values.astype(np.float32)

    # Treatment → action
    treatment = get_treatment_combo(row)
    action = treatment_mapping[treatment]

    # Reward
    reward = float(row["reward"])

    # Each row = single patient episode
    terminal = 1

    observations.append(state)
    actions.append(action)
    rewards.append(reward)
    terminals.append(terminal)

# Convert to numpy arrays
observations = np.array(observations, dtype=np.float32)
actions = np.array(actions, dtype=np.int64)
rewards = np.array(rewards, dtype=np.float32)
terminals = np.array(terminals, dtype=np.float32)

# Create MDPDataset
dataset = MDPDataset(observations, actions, rewards, terminals)

# Save pickle file
with open("../../data/episodes/all_treatment_episodes.pkl", "wb") as f:
    pickle.dump(dataset, f)

print("🎉 Saved RL dataset to all_treatment_episodes.pkl")
