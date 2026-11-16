# Verification Report

Generated in the Codex workspace on 2026-06-13.

## Static Verification

`python -m compileall src api app scripts tests` completed successfully.

## Unit-Style Checks

The following assertions passed:

- A tautology attack is detected.
- A legitimate template query is allowed.
- URL encoded `oR%201=1` is decoded and detected.

## Dependency-Light Cross-Dataset Demo

The bundled environment did not include scikit-learn, FastAPI, Streamlit, XGBoost, LightGBM, or SHAP, so the verification used the deterministic fallback hybrid scorer. Full model training is available after installing `requirements.txt`.

| Dataset | Accuracy | Precision | Recall | F1 | FPR | Avg Latency ms |
|---|---:|---:|---:|---:|---:|---:|
| B External Validation | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.552 |
| C Independent Public-Style | 0.833 | 1.000 | 0.750 | 0.857 | 0.000 | 0.411 |
| D Synthetic Obfuscated | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.505 |
| E Legitimate Production-Style | 1.000 | N/A | N/A | N/A | 0.000 | 0.913 |

Dataset E contains only benign samples; precision, recall, and F1 are not meaningful for the positive SQLi class on that set. The key reviewer metric for Dataset E is false-positive rate.

## Real-Time Benchmark

`python -m scripts.benchmark --iterations 500`

- Throughput: 2194.98 queries/second.
- Average latency: 0.4553 ms.
- p95 latency: 0.6728 ms.

## Direct Prediction Examples

| Query | Decision | Confidence | Threat |
|---|---|---:|---|
| `SELECT * FROM users WHERE id = 7` | ALLOW | 0.75% | LOW |
| `SELECT * FROM users WHERE id = 1 OR 1=1 --` | BLOCK | 57.54% | HIGH |
| `oR%201=1` | BLOCK | 78.90% | CRITICAL |
| `CHAR(49)=CHAR(49)` | BLOCK | 44.61% | HIGH |
| `UNION SELECT username,password FROM users` | BLOCK | 44.95% | HIGH |

