import pandas as pd
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

model = joblib.load("models/svm_model.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

df = pd.read_csv("data/cleaned/clean_dataset_B.csv")

X = df["payload"]
y = df["Label"]

X_vec = vectorizer.transform(X)

pred = model.predict(X_vec)

print("Evaluation Metrics:")

print("Accuracy:", accuracy_score(y, pred))
print("Precision:", precision_score(y, pred))
print("Recall:", recall_score(y, pred))
print("F1:", f1_score(y, pred))
print("Confusion Matrix:")
print(confusion_matrix(y, pred))

print("Evaluation completed successfully.")