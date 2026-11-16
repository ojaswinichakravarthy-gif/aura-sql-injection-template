"""Evaluation helpers for baseline, ablation, robustness, and cross-dataset reports."""

from __future__ import annotations

import csv
import time
from pathlib import Path

from .engine import DetectionEngine


def evaluate_csv(path: str | Path, engine: DetectionEngine | None = None) -> dict[str, float]:
    engine = engine or DetectionEngine()
    y_true: list[int] = []
    y_pred: list[int] = []
    latencies: list[float] = []
    with Path(path).open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            started = time.perf_counter()
            result = engine.detect(row["query"])
            latencies.append((time.perf_counter() - started) * 1000)
            y_true.append(1 if row["label"].lower() in {"sqli", "payload", "1"} else 0)
            y_pred.append(1 if result.decision in {"BLOCK", "SUSPICIOUS"} else 0)
    tp = sum(1 for a, b in zip(y_true, y_pred) if a == b == 1)
    tn = sum(1 for a, b in zip(y_true, y_pred) if a == b == 0)
    fp = sum(1 for a, b in zip(y_true, y_pred) if a == 0 and b == 1)
    fn = sum(1 for a, b in zip(y_true, y_pred) if a == 1 and b == 0)
    total = max(len(y_true), 1)
    precision = tp / max(tp + fp, 1)
    recall = tp / max(tp + fn, 1)
    f1 = 2 * precision * recall / max(precision + recall, 1e-9)
    return {
        "rows": float(total),
        "accuracy": (tp + tn) / total,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "false_positive_rate": fp / max(fp + tn, 1),
        "avg_latency_ms": sum(latencies) / max(len(latencies), 1),
    }
