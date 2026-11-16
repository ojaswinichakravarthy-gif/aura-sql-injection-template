# Dataset Manifest

| Dataset | Role | Used For Training | Description |
|---|---|---:|---|
| A | Primary Training Dataset | Yes | Balanced seed set for baseline and hybrid model fitting |
| B | External Validation Dataset | No in strict test | Distribution-shift validation queries |
| C | Independent Public Dataset | No | Public-style independent SQLi and benign queries |
| D | Synthetic Obfuscated SQLi Dataset | No | URL, comment, hex, whitespace, nested, and function-encoded attacks |
| E | Legitimate Production Query Dataset | No | Benign production-style query templates for false-positive evaluation |

The strict reviewer protocol trains only on Dataset A and tests on B-E. A broader production model may train on A plus approved historical production data, then reserve C-D for independent robustness testing and E for false-positive monitoring.

