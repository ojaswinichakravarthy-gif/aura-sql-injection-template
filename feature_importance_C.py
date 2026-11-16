import joblib
import pandas as pd

MODEL_PATH = "models/model.joblib"

artifact = joblib.load(MODEL_PATH)

model = artifact["model"]
feature_order = artifact["feature_order"]

if not hasattr(model, "feature_importances_"):
	raise ValueError(f"Model type {type(model).__name__} does not expose feature_importances_.")


importance_df = pd.DataFrame(
{
"Feature": feature_order,
"Importance": model.feature_importances_,
}
)

importance_df = (
importance_df
.sort_values("Importance", ascending=False)
.reset_index(drop=True)
)

print("\nTop Feature Importances\n")
print(importance_df.head(15))

importance_df.to_csv(
"reports/feature_importance_C.csv",
index=False
)

print(
"\nSaved feature importance table to "
"reports/feature_importance_C.csv"
)
