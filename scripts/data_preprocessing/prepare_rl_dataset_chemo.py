import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from d3rlpy.dataset import MDPDataset


# Load cleaned dataset
df = pd.read_csv("../../data/cleaned_metabric_chemo.csv")

# Define state, action, reward
state_cols = ['Age at Diagnosis', 'Tumor Size', 'Neoplasm Histologic Grade', 'ER Status', 'PR Status', 'HER2 Status']
action_col = 'Chemotherapy'
reward_col = 'Reward'

# Convert data into arrays
states = df[state_cols].values
actions = df[action_col].values.reshape(-1, 1)  # Discrete actions
rewards = df[reward_col].values
terminals = np.array([True] * len(df))  # Assume all are terminal since it's offline

# Create MDP Dataset for d3rlpy
dataset = MDPDataset(states, actions, rewards, terminals)

import pickle
# Number of episodes
print(len(dataset.episodes))

#save episodes
with open('../../data/episodes/chemo_episodes.pkl', 'wb') as f:
    pickle.dump(dataset.episodes, f)


# First episode details
episode = dataset.episodes[0]
print("States:", episode.observations)
print("Actions:", episode.actions)
print("Rewards:", episode.rewards)
print("Terminated:", episode.terminated)

