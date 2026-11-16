# analyze_false_negatives.py

import pandas as pd
import joblib

model = joblib.load("models/svm_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

df = pd.read_csv("data/cleaned/clean_dataset_B.csv")

X = df["payload"]
y = df["Label"]

X_vec = vectorizer.transform(X)

pred = model.predict(X_vec)

# False negatives:
# Actual = 1 (SQLi)
# Predicted = 0 (Normal)

false_negatives = df[(y == 1) & (pred == 0)]

print("False Negatives:", len(false_negatives))

false_negatives.to_csv("data/false_negatives.csv", index=False)

print("Saved.")