from pathlib import Path
import json
import pandas as pd
import joblib

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
accuracy_score,
precision_score,
recall_score,
f1_score,
roc_auc_score,
)
from sklearn.model_selection import train_test_split

DATASET = "data/aura_dataset_A.csv"
OUTPUT = Path("ablation_study/lexical_only")

LEXICAL_FEATURES = [
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
]

OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATASET)

X = df[LEXICAL_FEATURES]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
X,
y,
test_size=0.2,
stratify=y,
random_state=42,
)

model = RandomForestClassifier(
n_estimators=300,
random_state=42,
class_weight="balanced",
)

model.fit(X_train, y_train)

proba = model.predict_proba(X_test)[:, 1]
pred = (proba >= 0.5).astype(int)

metrics = {
"accuracy": float(accuracy_score(y_test, pred)),
"precision": float(precision_score(y_test, pred)),
"recall": float(recall_score(y_test, pred)),
"f1": float(f1_score(y_test, pred)),
"roc_auc": float(roc_auc_score(y_test, proba)),
}

joblib.dump(model, OUTPUT / "model.joblib")

with open(OUTPUT / "metrics.json", "w") as f:
    json.dump(metrics, f, indent=2)

print(json.dumps(metrics, indent=2))
