# Ablation Plan

Run the following configurations:

| Configuration | Disabled Component | Expected Observation |
|---|---|---|
| Full Hybrid | None | Best robustness and explainability |
| Without Structural Delta | Template-derived delta features | Lower recall on obfuscated and unseen attacks |
| Without Template Matching | Aura template similarity/mismatch | Higher false positives or weaker structural reasoning |
| Without Ensemble | Use SVM only | Baseline comparison to NLP-SVM paper |
| Without Explainability | Explanation layer | Similar metrics but weaker deployability and reviewability |

Implementation approach:

1. Generate feature matrix with `scripts/featurize_dataset.py`.
2. Remove ablated feature columns before training.
3. Train the same candidate model families.
4. Evaluate on B-E without retuning.
5. Report metrics and latency in `docs/ieee_results.md`.

