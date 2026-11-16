"""Layer 5: model training, ensemble selection, and dependency-light fallback."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any




FEATURE_ORDER = [
    "query_length", "token_count", "token_diversity", "query_entropy", "special_char_density",
    "sql_keyword_count", "sql_keyword_ratio", "operator_count", "suspicious_token_count",
    "quote_count", "comment_removed", "url_decode_layers", "sig_tautology", "sig_union_select",
    "sig_stacked_query", "sig_comment_truncation", "sig_time_based", "sig_metadata_probe",
    "signature_count", "template_similarity", "template_mismatch", "structural_delta",
    "extra_control_keywords", "predicate_complexity", "tautology_detected", "stacked_query_detected",
]


@dataclass(frozen=True)
class ModelPrediction:
    label: str
    score: float
    model_name: str
    component_scores: dict[str, float]


class HeuristicEnsemble:
    """Transparent fallback used for demos before the trained model artifact exists."""

    name = "heuristic-weighted-hybrid"

    weights = {
        "signature_count": 0.18,
        "sig_union_select": 0.16,
        "sig_tautology": 0.14,
        "sig_stacked_query": 0.13,
        "tautology_detected": 0.16,
        "stacked_query_detected": 0.14,
        "suspicious_token_count": 0.08,
        "template_mismatch": 0.11,
        "structural_delta": 0.12,
        "extra_control_keywords": 0.05,
        "url_decode_layers": 0.03,
        "comment_removed": 0.02,
    }

    def predict(self, features: dict[str, float]) -> ModelPrediction:
        raw = 0.0
        component_scores: dict[str, float] = {}
        for name, weight in self.weights.items():
            if name == "suspicious_token_count":
                value = min(float(features.get(name, 0.0)), 3.0) / 3.0
            elif name.endswith("_count"):
                value = min(float(features.get(name, 0.0)), 1.0)
            else:
                value = float(features.get(name, 0.0))
            contribution = weight * max(0.0, min(value, 1.0))
            component_scores[name] = contribution
            raw += contribution
        if features.get("template_similarity", 1.0) < 0.50:
            raw += 0.08
            component_scores["low_template_similarity"] = 0.08
        score = max(0.0, min(raw, 1.0))
        if score >= 0.42:
            label = "BLOCK"
        elif score >= 0.25:
            label = "SUSPICIOUS"
        else:
            label = "ALLOW"
        return ModelPrediction(label, score, self.name, component_scores)

def train_research_models(dataset_path: str | Path, output_dir: str | Path) -> dict[str, Any]:
    """Train baseline SVM and full ensemble when optional ML dependencies are installed."""

    try:
        import joblib
        import pandas as pd
        from sklearn.ensemble import RandomForestClassifier, StackingClassifier, VotingClassifier
        from sklearn.linear_model import LogisticRegression
        from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
        from sklearn.model_selection import train_test_split
        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler
        from sklearn.svm import SVC
    except Exception as exc:
        raise RuntimeError(
            "Training requires optional research dependencies. Install requirements.txt first."
        ) from exc

    output = Path(output_dir)
    output.mkdir(parents=True, exist_ok=True)

    data = pd.read_csv(dataset_path)

    X = data[FEATURE_ORDER]
    y = data["label"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        stratify=y,
        test_size=0.2,
        random_state=42
    )

    models: dict[str, Any] = {
        "baseline_svm": Pipeline([
            ("scale", StandardScaler()),
            ("clf", SVC(probability=True, kernel="rbf", C=6.5))
        ]),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            random_state=42,
            class_weight="balanced"
        ),
    }

    try:
        from xgboost import XGBClassifier
        models["xgboost"] = XGBClassifier(
            n_estimators=250,
            max_depth=5,
            learning_rate=0.05,
            eval_metric="logloss"
        )
    except Exception:
        pass

    try:
        from lightgbm import LGBMClassifier
        models["lightgbm"] = LGBMClassifier(
            n_estimators=250,
            learning_rate=0.05,
            class_weight="balanced"
        )
    except Exception:
        pass

    fitted = {}
    metrics = {}

    for name, model in models.items():
        model.fit(X_train, y_train)

        proba = model.predict_proba(X_test)[:, 1]
        pred = (proba >= 0.5).astype(int)

        metrics[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "precision": float(precision_score(y_test, pred)),
            "recall": float(recall_score(y_test, pred)),
            "f1": float(f1_score(y_test, pred)),
            "roc_auc": float(roc_auc_score(y_test, proba)),
        }

        fitted[name] = model

    estimators = [(name, model) for name, model in fitted.items()]

    voting = VotingClassifier(
        estimators=estimators,
        voting="soft"
    )

    stacking = StackingClassifier(
        estimators=estimators,
        final_estimator=LogisticRegression(max_iter=1000)
    )

    candidates = {
        "soft_voting": voting,
        "stacking": stacking
    }

    for name, model in candidates.items():
        model.fit(X_train, y_train)

        proba = model.predict_proba(X_test)[:, 1]
        pred = (proba >= 0.5).astype(int)

        metrics[name] = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "precision": float(precision_score(y_test, pred)),
            "recall": float(recall_score(y_test, pred)),
            "f1": float(f1_score(y_test, pred)),
            "roc_auc": float(roc_auc_score(y_test, proba)),
        }

        fitted[name] = model

    best_name = max(metrics, key=lambda name: metrics[name]["f1"])

    joblib.dump(
        {
            "model": fitted[best_name],
            "feature_order": FEATURE_ORDER,
            "best_name": best_name,
        },
        output / "model.joblib"
    )

    (output / "metrics.json").write_text(
        json.dumps(
            {
                "best": best_name,
                "metrics": metrics,
            },
            indent=2
        ),
        encoding="utf-8"
    )

    return {
        "best": best_name,
        "metrics": metrics,
    }