import pandas as pd

df = pd.read_csv("data/cleaned/clean_dataset_B.csv")

print(df.head(20))
print(df["Label"].value_counts())
print(df.sample(20))
df["Label"].value_counts()