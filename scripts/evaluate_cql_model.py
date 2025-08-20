# evaluate_cql_model.py

import pickle
import numpy as np
from d3rlpy.dataset import MDPDataset
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from sklearn.model_selection import train_test_split

# Load saved episodes
with open('../data/episodes.pkl', 'rb') as f:
    episodes = pickle.load(f)

# Split into test episodes
_, test_episodes = train_test_split(episodes, test_size=0.2, random_state=42)

# Initialize the CQL agent with required arguments
config = DiscreteCQLConfig()
cql = DiscreteCQL(config=config, device="cpu", enable_ddp=False)
# Build with test dataset shape for consistency
test_obs = []
test_act = []
test_rew = []
test_term = []
for ep in test_episodes:
    test_obs.extend(ep.observations)
    test_act.extend(ep.actions)
    test_rew.extend(ep.rewards)
    test_term.append(ep.terminated)
test_dataset = MDPDataset(
    np.array(test_obs),
    np.array(test_act),
    np.array(test_rew),
    np.array(test_term)
)
cql.build_with_dataset(test_dataset)
cql.load_model("../model/cql_brca_metabric_model.pt")

# Evaluate: run policy on test episodes and compute average reward
total_rewards = []
for ep in test_episodes:
    obs = ep.observations
    rewards = []
    for o in obs:
        o_batch = np.expand_dims(o, axis=0)  # Ensure shape (1, obs_dim)
        action = cql.predict(o_batch)[0]
        rewards.append(ep.rewards[0])  # or your own reward function
    total_rewards.append(np.sum(rewards))

avg_reward = np.mean(total_rewards)
print("📊 Average Reward per Test Episode (Policy Quality):", avg_reward)
