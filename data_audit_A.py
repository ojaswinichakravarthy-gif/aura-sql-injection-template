import pandas as pd

df = pd.read_csv("dataset_A.csv")

print("Total Rows:", len(df))

print("\nColumns:")
print(df.columns)

print("\nLabel Distribution:")
print(df["Label"].value_counts())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Queries:")
print(df.duplicated(subset=["Sentence"]).sum())

# ADD THESE THREE

print("\n===== HEAD =====")
print(df.head())

print("\n===== FIRST ROW =====")
print(df.iloc[0])

print("\n===== DATA TYPES =====")
print(df.dtypes)

print("\nRows with missing Label:")
print(df["Label"].isna().sum())

print("\nRows with data in Unnamed: 2:")
print(df["Unnamed: 2"].notna().sum())

print("\nRows with data in Unnamed: 3:")
print(df["Unnamed: 3"].notna().sum())