# measure_model_confidence_all.py

import pickle
import numpy as np
from d3rlpy.dataset import MDPDataset
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from sklearn.model_selection import train_test_split
from scipy.special import softmax

# === Load test data (all treatments) ===
with open("../data/episodes/all_treatment_episodes.pkl", "rb") as f:
    obj = pickle.load(f)

episodes = obj.episodes if hasattr(obj, "episodes") else obj
_, test_episodes = train_test_split(episodes, test_size=0.2, random_state=42)

# Flatten all observations
test_obs = []
for ep in test_episodes:
    test_obs.extend(ep.observations)  # each is (1, 6)
test_obs = np.array(test_obs)

# === Load model ===
config = DiscreteCQLConfig()
cql = DiscreteCQL(config=config, device="cpu", enable_ddp=False)

# Ensure action size is 8 when building
num_actions = 8
# Repeat 0..7 across the test set to include all actions
dummy_act = np.resize(np.arange(num_actions, dtype=np.int64), len(test_obs))

dummy_dataset = MDPDataset(
    test_obs,
    dummy_act,
    np.zeros(len(test_obs), dtype=np.float32),
    np.ones(len(test_obs), dtype=bool),
)
cql.build_with_dataset(dummy_dataset)

# Load the trained checkpoint (.d3)
cql.load_model("../model/all_cql_brca_metabric_model.d3")

# Predicted actions (not strictly needed for margins, but useful)
pred_actions = cql.predict(test_obs)

# Compute Q-values for all 8 actions for each observation
q_values_all = np.stack(
    [cql.predict_value(test_obs, np.full(len(test_obs), a, dtype=np.int64)) for a in range(num_actions)],
    axis=1,
)  # shape: (n, 8)

# Confidence as margin between best and second-best Q
top_idx = np.argmax(q_values_all, axis=1)
top_q = q_values_all[np.arange(len(q_values_all)), top_idx]
second_q = np.partition(q_values_all, -2, axis=1)[:, -2]
conf_margins = top_q - second_q
mean_margin = np.mean(conf_margins)

# Softmax-based approximate confidence
softmax_conf = [np.max(softmax(q)) for q in q_values_all]
mean_softmax_conf = np.mean(softmax_conf) * 100

print("Min Q-value Margin:", round(np.min(conf_margins), 3))
print("Max Q-value Margin:", round(np.max(conf_margins), 3))
print("Average Q-value Margin (Decision Confidence):", round(mean_margin, 3))
print("Approximate Model Confidence (Softmax %):", round(mean_softmax_conf, 2), "%")
