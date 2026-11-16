import json
import pandas as pd

lexical = json.load(
open("ablation_study/lexical_only/metrics.json")
)

structural = json.load(
open("ablation_study/structural_only/metrics.json")
)

full = json.load(
open("models/metrics.json")
)

results = pd.DataFrame(
[
{
"Model": "Lexical Only",
**lexical,
},
{
"Model": "Structural Only",
**structural,
},
{
"Model": "Full Aura",
**full["metrics"][full["best"]],
},
]
)

print("\nAblation Study Results\n")
print(results)

results.to_csv(
"ablation_study/ablation_comparison.csv",
index=False,
)

print(
"\nSaved to ablation_study/ablation_comparison.csv"
)
