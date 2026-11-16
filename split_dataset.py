import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("data/cleaned/clean_dataset_A.csv")

train_df, test_df = train_test_split(
    df,
    test_size=0.2,
    stratify=df["Label"],
    random_state=42
)

train_df.to_csv("data/train_A.csv", index=False)
test_df.to_csv("data/test_A.csv", index=False)

print("Training rows:", len(train_df))
print("Testing rows:", len(test_df))