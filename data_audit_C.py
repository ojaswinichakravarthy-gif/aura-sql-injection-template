import pandas as pd

df = pd.read_csv("data/raw/dataset_c.csv")

print(df.columns)
print(df.shape)
print(df.head())
print(df["label"].value_counts())