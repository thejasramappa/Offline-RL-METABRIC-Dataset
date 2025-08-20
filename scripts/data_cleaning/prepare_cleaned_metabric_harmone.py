import pandas as pd

# Load original data
df = pd.read_csv("../../data/Brca_metabric_clinical_data.tsv", sep="\t")

# Features to keep (Hormone Therapy only)
features = [
    'Age at Diagnosis',                 # Numeric
    'Tumor Size',                       # Numeric
    'Neoplasm Histologic Grade',        # Numeric (1–3)
    'ER Status', 'PR Status', 'HER2 Status',  # Categorical → 0/1
    'Hormone Therapy',                  # Action (only this treatment)
    "Patient's Vital Status"            # → reward
]

# Drop rows with missing values in selected columns
df = df[features].dropna()

# Encode categorical features
df['ER Status'] = df['ER Status'].map({'Positive': 1, 'Negative': 0})
df['PR Status'] = df['PR Status'].map({'Positive': 1, 'Negative': 0})
df['HER2 Status'] = df['HER2 Status'].map({'Positive': 1, 'Negative': 0})

# Encode Hormone Therapy YES/NO → 1/0
df['Hormone Therapy'] = df['Hormone Therapy'].map({'YES': 1, 'NO': 0})

# Keep only patients with clear survival outcome
df = df[df["Patient's Vital Status"].isin(['Living', 'Died of Disease'])]

# Create Reward column (Living → 1, Died of Disease → 0)
df['Reward'] = df["Patient's Vital Status"].map({'Living': 1, 'Died of Disease': 0})

# Drop the original survival column
df = df.drop(columns=["Patient's Vital Status"])

# Save cleaned dataset
df.to_csv("../../data/cleaned_metabric_hormone.csv", index=False)
print("✅ Cleaned dataset (Hormone Therapy only) saved as 'data/cleaned_metabric_hormone.csv'")
