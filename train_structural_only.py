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
OUTPUT = Path("ablation_study/structural_only")

STRUCTURAL_FEATURES = [
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

OUTPUT.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(DATASET)

X = df[STRUCTURAL_FEATURES]
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
