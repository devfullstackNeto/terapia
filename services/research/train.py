"""Reproducible, non-clinical engagement model demonstration on synthetic data only."""
import json
from datetime import date
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

root = Path(__file__).resolve().parents[2]
data = json.loads((root / "data" / "terapia_synthetic_v3.json").read_text(encoding="utf-8"))
assert "100% SYNTHETIC" in data["metadata"]["warning"]
users = {u["user_id"]: u for u in data["users"]}
features = []
labels = []
for user_id, user in users.items():
    cutoff = date.fromisoformat("2026-06-29")
    before = lambda row: date.fromisoformat(row["date"]) < cutoff
    after = lambda row: date.fromisoformat(row["date"]) >= cutoff
    checkins = sum(x["user_id"] == user_id and before(x) for x in data["mood_checkins"])
    care = sum(x["user_id"] == user_id and before(x) for x in data["selfcare_uses"])
    appointments = sum(x["user_id"] == user_id and before(x) for x in data["appointments"])
    future_activity = sum(x["user_id"] == user_id and after(x) for x in data["mood_checkins"])
    future_activity += sum(x["user_id"] == user_id and after(x) for x in data["selfcare_uses"])
    features.append([checkins, care, appointments, int(user["notification_opt_in"])])
    labels.append(int(future_activity >= 6))  # future engagement only; never clinical state
cv = StratifiedKFold(5, shuffle=True, random_state=42)
models = {"logistic_regression": LogisticRegression(max_iter=1000, random_state=42), "random_forest": RandomForestClassifier(n_estimators=200, random_state=42, max_depth=5)}
result = {"banner": "NON-CLINICAL • DADOS SINTÉTICOS", "target": "engagement_next_7_days", "baseline_accuracy": max(sum(labels), len(labels)-sum(labels))/len(labels), "models": {}}
for name, model in models.items():
    pred = cross_val_predict(model, features, labels, cv=cv, method="predict")
    prob = cross_val_predict(model, features, labels, cv=cv, method="predict_proba")[:, 1]
    model.fit(features, labels)
    importance = model.feature_importances_.tolist() if hasattr(model, "feature_importances_") else [abs(x) for x in model.coef_[0]]
    result["models"][name] = {"accuracy": accuracy_score(labels, pred), "roc_auc": roc_auc_score(labels, prob), "feature_importance": importance}
print(json.dumps(result, indent=2))
