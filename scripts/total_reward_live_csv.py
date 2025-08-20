import pandas as pd

# Load CSV
df = pd.read_csv("../data/live_predictions_log.csv")

# Replace only NaN in 'Reward' column with 0
df['Reward'] = df['Reward'].fillna(0).astype(int)

# Display updated data
print("\n📋 All Patient Records (with Reward 0 or 1):\n")
print(df.to_string(index=False))

# Count rewards
reward_counts = df['Reward'].value_counts()
print(f"\n✅ Reward Summary:")
for val, count in sorted(reward_counts.items()):
    print(f"  Reward = {val}: {count} entries")
