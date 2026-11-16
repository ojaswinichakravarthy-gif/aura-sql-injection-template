import pandas as pd
df = pd.read_csv("dataset_B.csv")

df_b = df[df["attack_type"].isin(["norm", "sqli"])]
df_b["Label"] = df_b["attack_type"].map({
    "norm": 0,
    "sqli": 1
})
df_b = df_b[["payload", "Label"]]

print(df_b["Label"].value_counts())
print(len(df_b))

df_b.to_csv("clean_dataset_B.csv", index=False)
print("Cleaned dataset saved to clean_dataset_B.csv")
