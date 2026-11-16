import pandas as pd

df = pd.read_csv("dataset_A.csv")
# Remove rows with missing labels
df["Label"] = df["Label"].fillna(df["Unnamed: 2"])
df = df[["Sentence", "Label"]]
df = df.dropna()
df = df[df["Label"].isin(["0", "1", 0, 1])]
df["Label"] = df["Label"].astype(int)
df = df.drop_duplicates(subset=["Sentence"])
print(df["Label"].value_counts())
print(df.isnull().sum())
print(len(df))
df.to_csv("clean_dataset_A.csv", index=False)
print("Cleaned dataset saved to clean_dataset_A.csv")