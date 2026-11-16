import pandas as pd

df = pd.read_csv("payload_full.csv")

print(df["attack_type"].value_counts())
print("\n")
print(df["label"].value_counts())