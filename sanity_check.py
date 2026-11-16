import pandas as pd

df = pd.read_csv("data/aura_dataset_A.csv")

print(df.groupby("label").mean())