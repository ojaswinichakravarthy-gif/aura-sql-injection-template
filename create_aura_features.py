import pandas as pd

from src.normalization import QueryNormalizer
from src.feature_extractor import SemanticFeatureExtractor
from src.structural_delta import StructuralDeltaAnalyzer

print("Loading dataset...")

df = pd.read_csv("data/cleaned/clean_dataset_A.csv")

normalizer = QueryNormalizer()
semantic_extractor = SemanticFeatureExtractor()
structural_analyzer = StructuralDeltaAnalyzer()

feature_rows = []

for _, row in df.iterrows():

    query = str(row["Sentence"])
    label = row["Label"]

    normalized = normalizer.normalize(query)

    semantic_features = semantic_extractor.extract(
        normalized
    ).values

    structural_features, template_match = (
        structural_analyzer.analyze(normalized)
    )

    features = {
        **semantic_features,
        **structural_features.as_features(),
        "label": label
    }

    feature_rows.append(features)

feature_df = pd.DataFrame(feature_rows)

feature_df.to_csv(
    "data/aura_dataset_A.csv",
    index=False
)

print("Aura feature dataset created.")
print(f"Feature dataset shape: {feature_df.shape}")
print(feature_df.columns.tolist())
print(feature_df.head())