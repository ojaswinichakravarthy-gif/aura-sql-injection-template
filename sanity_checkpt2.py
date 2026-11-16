import pandas as pd

df = pd.read_csv("data/aura_dataset_A.csv")

important = [
    "template_similarity",
    "structural_delta",
    "signature_count",
    "suspicious_token_count",
    "sql_keyword_count",
    "sig_union_select",
    "sig_time_based",
    "sig_metadata_probe"
]

print(df.groupby("label")[important].mean())