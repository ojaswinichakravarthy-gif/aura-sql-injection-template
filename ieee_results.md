# IEEE Results Section Template

The framework reports accuracy, precision, recall, F1 score, ROC-AUC, false-positive rate, average latency, p95 latency, throughput, and memory usage. Results should be presented in four experiment groups:

1. Baseline SVM Experiment: reproduces the baseline NLP-SVM philosophy using only semantic/NLP features.
2. Ensemble Experiment: evaluates Random Forest, XGBoost, LightGBM, soft voting, weighted voting, and stacking on fused features.
3. Structural Delta Experiment: evaluates the added value of template similarity, template mismatch, and structural delta features.
4. Full Hybrid Architecture Experiment: evaluates the complete system with normalization, semantic features, Aura templates, structural delta, ensemble learning, and explainability.

Recommended table:

| Experiment | Accuracy | Precision | Recall | F1 | ROC-AUC | FPR | Avg Latency ms |
|---|---:|---:|---:|---:|---:|---:|---:|
| NLP-SVM baseline | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Ensemble only | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Structural delta only | TBD | TBD | TBD | TBD | TBD | TBD | TBD |
| Full hybrid | TBD | TBD | TBD | TBD | TBD | TBD | TBD |

Cross-dataset generalization should be reported separately:

| Train Set | Test Set | Purpose | F1 | FPR | Avg Latency ms |
|---|---|---|---:|---:|---:|
| A | B | external validation | TBD | TBD | TBD |
| A | C | independent public dataset | TBD | TBD | TBD |
| A | D | obfuscated unseen attacks | TBD | TBD | TBD |
| A | E | production legitimate queries | TBD | TBD | TBD |

The concrete workspace verification results are recorded in `docs/verification_report.md`. Those values use the deterministic dependency-light hybrid scorer. Final publication values should be regenerated after installing `requirements.txt` and training the SVM/ensemble models on the selected full datasets.
