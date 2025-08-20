import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from d3rlpy.dataset import MDPDataset
import pickle

# Load cleaned dataset (Hormone Therapy only)
df = pd.read_csv("../../data/cleaned_metabric_hormone.csv")

# Define state, action, reward
state_cols = ['Age at Diagnosis', 'Tumor Size', 'Neoplasm Histologic Grade',
              'ER Status', 'PR Status', 'HER2 Status']
action_col = 'Hormone Therapy'  
reward_col = 'Reward'

# Convert data into arrays
states = df[state_cols].values
actions = df[action_col].values.reshape(-1, 1)  # Discrete actions (YES/NO → 1/0)
rewards = df[reward_col].values
terminals = np.array([True] * len(df))  # Each patient is a terminal state

# Create MDP Dataset for d3rlpy
dataset = MDPDataset(states, actions, rewards, terminals)

# Print number of episodes
print("Number of episodes:", len(dataset.episodes))

# Save episodes to pickle
with open("../../data/episodes/hormone_episodes.pkl", "wb") as f:
    pickle.dump(dataset.episodes, f)

# Inspect first episode
episode = dataset.episodes[0]
print("States:", episode.observations)
print("Actions:", episode.actions)
print("Rewards:", episode.rewards)
print("Terminated:", episode.terminated)
