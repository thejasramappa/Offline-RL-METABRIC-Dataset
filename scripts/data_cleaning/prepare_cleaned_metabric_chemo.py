import pandas as pd

# Loading original data
df = pd.read_csv("../../data/Brca_metabric_clinical_data.tsv", sep='\t')


# Features to keep
features = [
    'Age at Diagnosis',                 # Numeric
    'Tumor Size',                       # Numeric
    'Neoplasm Histologic Grade',       # Numeric (1–3)
    'ER Status', 'PR Status', 'HER2 Status',  # Categorical → 0/1
    'Chemotherapy',                    # Action
    "Patient's Vital Status"          # → reward
]


# Droping rows with any missing values in selected columns
df = df[features].dropna()

# Encoding categorical features
df['ER Status'] = df['ER Status'].map({'Positive': 1, 'Negative': 0})
df['PR Status'] = df['PR Status'].map({'Positive': 1, 'Negative': 0})
df['HER2 Status'] = df['HER2 Status'].map({'Positive': 1, 'Negative': 0})
df['Chemotherapy'] = df['Chemotherapy'].map({'YES': 1, 'NO': 0})


# Filtering rows we can use
df = df[df["Patient's Vital Status"].isin(['Living', 'Died of Disease'])]

# Creating reward column
df['Reward'] = df["Patient's Vital Status"].map({'Living': 1, 'Died of Disease': 0})

# Drop the original survival column (you've used it to create Reward)
df = df.drop(columns=["Patient's Vital Status"])

# Saving cleaned data to a new CSV file
df.to_csv("../../data/cleaned_metabric_chemo.csv", index=False)
print("✅ Cleaned dataset saved as 'cleaned_metabric_chemo.csv'")
