import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from d3rlpy.algos import DiscreteCQL, DiscreteCQLConfig
from d3rlpy.dataset import MDPDataset
import torch

# 1) Load episodes
episodes_path = os.path.join(os.path.dirname(__file__), "..", "data", "episodes", "all_treatment_episodes.pkl")
with open(episodes_path, "rb") as f:
    obj = pickle.load(f)

episodes = obj.episodes if hasattr(obj, "episodes") else obj
print("✅ Loaded dataset:")
print("   # Episodes:", len(episodes))
first_ep = episodes[0]
obs_shape = first_ep.observations[0].shape
action_size = int(max(int(ep.actions.max()) for ep in episodes)) + 1
print("   Observation dim:", obs_shape)
print("   Action dim:", action_size)

# 2) Train / test split
train_eps, test_eps = train_test_split(episodes, test_size=0.2, random_state=42)
print(f"📊 Train episodes: {len(train_eps)}, Test episodes: {len(test_eps)}")

# 3) Build datasets (reference style)
def flatten(episode_list):
    obs, act, rew, term = [], [], [], []
    for ep in episode_list:
        obs.extend(ep.observations)   # (1, obs_dim)
        act.extend(ep.actions)        # (1,) or (1,1) ints 0..7
        rew.extend(ep.rewards)        # (1,)
        term.append(ep.terminated)    # bool
    obs = np.asarray(obs, dtype=np.float32)
    act = np.asarray(act)
    if act.ndim == 1:
        act = act.reshape(-1, 1)
    act = act.astype(np.int64)
    rew = np.asarray(rew, dtype=np.float32)
    term = np.asarray(term, dtype=bool)
    return obs, act, rew, term

train_obs, train_act, train_rew, train_term = flatten(train_eps)
test_obs, test_act, test_rew, test_term = flatten(test_eps)

train_dataset = MDPDataset(train_obs, train_act, train_rew, train_term)
test_dataset = MDPDataset(test_obs, test_act, test_rew, test_term)

# 4) Configure and create agent (same as train_cql_model.py)
config = DiscreteCQLConfig()
device = "cuda" if torch.cuda.is_available() else "cpu"
enable_ddp = False
cql = DiscreteCQL(config, device, enable_ddp)

# 5) Train (no logdir / no eval_episodes to match your d3rlpy)
cql.fit(
    train_dataset,
    n_steps=50000
)

# 6) Save models
model_dir = os.path.join(os.path.dirname(__file__), "..", "model")
os.makedirs(model_dir, exist_ok=True)

d3_path = os.path.join(model_dir, "all_cql_brca_metabric_model.d3")
cql.save_model(d3_path)
print("💾 Saved d3rlpy model:", d3_path)

# Optional: save raw torch weights (best-effort)
try:
    import torch as _torch
    _torch.save(cql.impl.q_func.state_dict(), os.path.join(model_dir, "all_cql_brca_metabric_model.pt"))
except Exception:
    pass

print("🎉 Training complete.")
