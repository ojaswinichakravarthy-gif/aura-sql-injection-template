import pandas as pd

from src.normalization import QueryNormalizer
from src.feature_extractor import SemanticFeatureExtractor
from src.structural_delta import StructuralDeltaAnalyzer

df = pd.read_csv("data/cleaned/clean_dataset_B.csv")
df.columns = df.columns.str.lower()
print(f"Loaded dataset with shape: {df.shape}")
print(df.columns.tolist())

normalizer = QueryNormalizer()
extractor = SemanticFeatureExtractor()
structural = StructuralDeltaAnalyzer()

rows = []

for _, row in df.iterrows():
    normalized = normalizer.normalize(row["payload"])

    semantic = extractor.extract(normalized).values

    delta, _ = structural.analyze(normalized)

    features = {
        **semantic,
        **delta.as_features(),
        "label": row["label"]
    }

    rows.append(features)

pd.DataFrame(rows).to_csv(
    "data/aura_dataset_B.csv",
    index=False
)

print(f"Dataset columns: {df.columns.tolist()}")
print(df.shape)
print(df.head())