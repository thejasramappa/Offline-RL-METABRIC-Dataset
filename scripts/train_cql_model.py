import pickle
import numpy as np
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from sklearn.model_selection import train_test_split
from d3rlpy.dataset import MDPDataset


# Set up CQL config and device
config = DiscreteCQLConfig()
device = "cpu"  # Use "cuda" if you have a GPU
enable_ddp = False

# Load saved episodes
with open('../data/episodes/hormone_episodes.pkl', 'rb') as f:
    episodes = pickle.load(f)

# Split episodes for training and testing
train_episodes, test_episodes = train_test_split(episodes, test_size=0.2)

# Convert episode objects to arrays for MDPDataset
def flatten_episodes(episodes):
    observations = []
    actions = []
    rewards = []
    terminals = []
    for ep in episodes:
        observations.extend(ep.observations)
        actions.extend(ep.actions)
        rewards.extend(ep.rewards)
        terminals.append(ep.terminated)
    return observations, actions, rewards, terminals

train_obs, train_act, train_rew, train_term = flatten_episodes(train_episodes)
test_obs, test_act, test_rew, test_term = flatten_episodes(test_episodes)

train_dataset = MDPDataset(
    np.array(train_obs),
    np.array(train_act),
    np.array(train_rew),
    np.array(train_term)
)
test_dataset = MDPDataset(
    np.array(test_obs),
    np.array(test_act),
    np.array(test_rew),
    np.array(test_term)
)

# Initialize CQL agent
cql = DiscreteCQL(config, device, enable_ddp)

# Train model
cql.fit(
    train_dataset,
    n_steps=50000
)

# Save the trained model
cql.save_model("../model/harmone_cql_brca_metabric_model.pt")
print("✅ CQL model trained and saved as 'radio_cql_brca_metabric_model.pt'")