import joblib
import pandas as pd

model_bundle = joblib.load(
    "models/aura-hybrid-1.0.0/model.joblib"
)

model = model_bundle["model"]

importance = pd.DataFrame({
    "Feature": model.feature_names_in_,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print(importance.head(15))