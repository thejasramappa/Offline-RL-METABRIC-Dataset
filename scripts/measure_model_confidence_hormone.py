# measure_model_confidence.py

import pickle
import numpy as np
from d3rlpy.dataset import MDPDataset
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from sklearn.model_selection import train_test_split


# === Load test data ===
with open("../data/episodes/hormone_episodes.pkl", "rb") as f:
    episodes = pickle.load(f)

_, test_episodes = train_test_split(episodes, test_size=0.2, random_state=42)

# Flatten all observations
test_obs = []
for ep in test_episodes:
    test_obs.extend(ep.observations)

test_obs = np.array(test_obs)

# === Load model ===
config = DiscreteCQLConfig()
cql = DiscreteCQL(config=config, device="cpu", enable_ddp=False)

# Ensure dummy actions include both 0 and 1
dummy_act = np.array([0, 1] * (len(test_obs) // 2 + 1))[:len(test_obs)]
dummy_dataset = MDPDataset(
    test_obs,
    dummy_act,
    np.zeros(len(test_obs), dtype=np.float32),
    np.ones(len(test_obs), dtype=bool)
)
cql.build_with_dataset(dummy_dataset)
cql.load_model("../model/hormone_cql_brca_metabric_model.pt")

# Get predicted actions for test observations
pred_actions = cql.predict(test_obs)

# Compute Q-values for each observation-action pair
q_values = cql.predict_value(test_obs, pred_actions)  # shape: (n,)

# For confidence, also get Q-values for both actions (0 and 1)
q_values_all = np.stack([
    cql.predict_value(test_obs, np.zeros(len(test_obs), dtype=int)),
    cql.predict_value(test_obs, np.ones(len(test_obs), dtype=int))
], axis=1)  # shape: (n, 2)

# margin = |Q1 - Q0| → confidence in decision
conf_margins = np.abs(q_values_all[:, 1] - q_values_all[:, 0])

# Mean margin = average confidence
mean_margin = np.mean(conf_margins)

# Normalize: use softmax gap as pseudo % confidence
from scipy.special import softmax
softmax_conf = [np.max(softmax(q)) for q in q_values_all]
mean_softmax_conf = np.mean(softmax_conf) * 100

print("Min Q-value Margin:", round(np.min(conf_margins), 3))
print("Max Q-value Margin:", round(np.max(conf_margins), 3))
print("Average Q-value Margin (Decision Confidence):", round(mean_margin, 3))
print("Approximate Model Confidence (Softmax %):", round(mean_softmax_conf, 2), "%")
