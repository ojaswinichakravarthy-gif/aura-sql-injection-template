# Reviewer Response Document

## Where is the proof of concept?

The proof of concept is implemented as a complete runnable framework. The core engine is in `src/aura_sqli`, the FastAPI service is in `api/main.py`, the Streamlit demo is in `app/streamlit_app.py`, and reproducibility scripts are in `scripts`. The sample datasets A-E demonstrate live prediction, cross-dataset testing, and obfuscated attack robustness.

## Where is the evidence of generalization?

The evaluation protocol trains on Dataset A and tests on B-E without retuning. Dataset B is external validation, Dataset C is independent public-style testing, Dataset D contains synthetic obfuscated attacks, and Dataset E contains legitimate production-style queries. The script `scripts/evaluate.py` produces the cross-dataset report.

## How deployment-ready is the system?

The system includes FastAPI real-time detection, batch detection, health checks, logging, Docker, Docker Compose, configuration files, model-versioned output directories, and latency/throughput benchmarking. The detector can run in a dependency-light mode for demonstrations and can load trained model artifacts in a production ML environment.

## Why were these datasets chosen?

The dataset split tests different claims. Dataset A supports supervised learning. Dataset B tests distribution shift. Dataset C tests independence from the training corpus. Dataset D tests adversarial obfuscation. Dataset E tests false-positive behavior on legitimate production-like SQL.

## What is the core research logic?

Legitimate SQL follows stable structural templates, while SQL injection changes structure, semantic intent, or logical flow. Therefore, detection should not rely only on NLP token patterns. Aura fuses NLP features with structural deltas against legitimate templates, then uses explainable ensemble learning for robust decisions.

## How is this different from existing NLP-SVM approaches?

The baseline paper uses NLP feature engineering and classical ML classifiers, selecting SVM by accuracy. Aura keeps that baseline but adds canonicalization against obfuscation, template intelligence, structural delta features, ensemble selection, explainability, deployment APIs, and cross-dataset generalization tests.

## What is the novelty contribution?

1. Structural Delta Detection Engine.
2. Aura Template Intelligence Layer.
3. Hybrid NLP plus structural feature fusion.
4. Explainable SQL injection decision reports.
5. Deployment-ready real-time detection framework.

## Can it detect unseen attacks?

Yes, the design targets unseen attacks by using behavior and structure, not only memorized tokens. Obfuscated examples such as `oR/**/1=1`, `oR%201=1`, `CHAR(49)=CHAR(49)`, hex payloads, URL encoding, whitespace manipulation, nested payloads, and `UNION SELECT` variants are included in Dataset D and the generator script.

## Can it explain its decisions?

Yes. Each prediction returns a reason, confidence score, threat level, influential features, and component scores. SHAP is included as a dependency for trained-model explanations in the full research environment.

## Can it operate in real time?

Yes. The dependency-light inference path is deterministic and low-latency. FastAPI exposes `/detect` for real-time use and `/detect/batch` for batch use. `scripts/benchmark.py` measures throughput and latency.

