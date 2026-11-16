# Aura SQLi Detection Framework

Hybrid Explainable Multi-Layer SQL Injection Detection Framework using NLP, Structural Delta Analysis, Aura Template Intelligence, and Ensemble Machine Learning.

This project extends the baseline paper **"Detection of SQL Injection Attack Using Machine Learning Based on Natural Language Processing"**. The baseline architecture is:

```text
Query -> NLP Feature Engineering -> ML Classifier -> SQLi Detection
```

Aura extends it into:

```text
Query
-> Normalization
-> Semantic/NLP Features
-> Aura Template Matching
-> Structural Delta Analysis
-> Ensemble Learning
-> Explainability
-> ALLOW / SUSPICIOUS / BLOCK
```

## What Is Implemented

- Layer 1 normalization: URL decoding, Unicode normalization, lowercase conversion, SQL comment removal, whitespace cleanup, tokenization, hex decoding, and obfuscation cleanup.
- Layer 2 semantic features: SQL keyword frequency, operator frequency, entropy, token diversity, special-character density, length, suspicious tokens, and injection signatures.
- Layer 3 Aura template database: legitimate SQL structures with query pattern, token sequence, and query-tree representation.
- Layer 4 structural delta: template mismatch, edit distance, control-flow expansion, predicate complexity, tautology, and stacked-query detection.
- Layer 5 ensemble learning: SVM baseline plus Random Forest, XGBoost, LightGBM, soft voting, and stacking when research dependencies are installed.
- Layer 6 explainability: deterministic local explanation reports plus SHAP integration point for trained models.
- Layer 7 decision layer: ALLOW, SUSPICIOUS, BLOCK with confidence, threat level, and influential features.
- FastAPI backend, Streamlit frontend, Docker files, health endpoint, batch API, benchmark script, model versioning path, sample datasets, ablation-ready scripts, and reviewer documents.

## Quick Local Demo

The core detector runs without heavy ML dependencies:

```powershell
$env:PYTHONPATH="src"
python -m scripts.evaluate --datasets data/sample/dataset_b_external.csv data/sample/dataset_d_synthetic_obfuscated.csv
python -m scripts.benchmark --iterations 1000
```

Full research training requires:

```powershell
pip install -r requirements.txt
$env:PYTHONPATH="src"
python -m scripts.featurize_dataset --input data/sample/dataset_a_primary.csv --output work/features_a.csv
python -m scripts.train --features work/features_a.csv --model-dir models/aura-hybrid-1.0.0
```

Run the API:

```powershell
$env:PYTHONPATH="src"
uvicorn api.main:app --host 0.0.0.0 --port 8000
```

Run the UI:

```powershell
$env:PYTHONPATH="src"
streamlit run app/streamlit_app.py
```

Docker:

```powershell
docker compose up --build
```

## Dataset Protocol

- Dataset A: primary training set.
- Dataset B: external validation set.
- Dataset C: independent public-style dataset.
- Dataset D: synthetic obfuscated SQLi variants.
- Dataset E: legitimate production-style query set.

Train on A only for the strict generalization experiment. Test B-E without tuning. Report per-dataset accuracy, precision, recall, F1, false-positive rate, and latency.

## Reviewer-Facing Claims

Proof of concept is provided by the executable engine, sample datasets, API/UI, tests, and benchmark scripts. Generalization is addressed by cross-dataset evaluation. Deployment readiness is addressed through FastAPI, Docker, logging, health checks, batch/real-time APIs, and latency measurement. Novelty comes from structural delta detection, Aura templates, feature fusion, explainable decisions, and production-oriented deployment.

