import pandas as pd

# Load Dataset C
df = pd.read_csv("data/raw/dataset_C.csv")

print("Original shape:", df.shape)
print(df.columns.tolist())

# Map Mendeley features to Aura features
feature_map = {
    "length": "query_length",
    "entropy": "query_entropy",
    "no_letter": "token_count",
    "no_keyword": "sql_keyword_count",
    "no_special _char": "special_char_density",
    "no_single_ qout": "quote_count",
    "no_comment": "comment_removed",
    "no_operat": "operator_count",
}

aura_df = pd.DataFrame()

# Copy mapped features
for source_col, target_col in feature_map.items():
    if source_col in df.columns:
        aura_df[target_col] = df[source_col]

# Aura features not present in Dataset C
missing_features = [
    "token_diversity",
    "sql_keyword_ratio",
    "suspicious_token_count",
    "url_decode_layers",
    "sig_tautology",
    "sig_union_select",
    "sig_stacked_query",
    "sig_comment_truncation",
    "sig_time_based",
    "sig_metadata_probe",
    "signature_count",
    "template_similarity",
    "template_mismatch",
    "structural_delta",
    "extra_control_keywords",
    "predicate_complexity",
    "tautology_detected",
    "stacked_query_detected"
]

for feature in missing_features:
    aura_df[feature] = 0

# Label
aura_df["label"] = df["label"]

# Ensure correct column order
FEATURE_ORDER = [
    "query_length",
    "token_count",
    "token_diversity",
    "query_entropy",
    "special_char_density",
    "sql_keyword_count",
    "sql_keyword_ratio",
    "operator_count",
    "suspicious_token_count",
    "quote_count",
    "comment_removed",
    "url_decode_layers",
    "sig_tautology",
    "sig_union_select",
    "sig_stacked_query",
    "sig_comment_truncation",
    "sig_time_based",
    "sig_metadata_probe",
    "signature_count",
    "template_similarity",
    "template_mismatch",
    "structural_delta",
    "extra_control_keywords",
    "predicate_complexity",
    "tautology_detected",
    "stacked_query_detected",
]

aura_df = aura_df[FEATURE_ORDER + ["label"]]

aura_df.to_csv(
    "data/aura_dataset_C.csv",
    index=False
)

print("Aura Dataset C created.")
print(aura_df.shape)
print(aura_df.head())