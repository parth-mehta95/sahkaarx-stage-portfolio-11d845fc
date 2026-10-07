"""
Model evaluation against quality thresholds and production criteria.
Incorporates PR #1 review feedback: Cross-validation scoring and strict threshold gates.
"""

from pathlib import Path
import json
import joblib
import numpy as np
from sklearn.model_selection import cross_val_score
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config
from src.data.preprocess import process_dataset
from src.utils.metrics import compute_classification_metrics, measure_inference_latency


def evaluate_model(profile_name: str | None = None) -> bool:
    """Evaluates the saved model against predefined performance criteria."""
    config = load_config()
    root = get_project_root()
    active_profile = profile_name or config.get("model", {}).get("active_profile", "production_regularized")
    model_path = root / config["model"]["artifacts_dir"] / config["model"]["model_filename"]

    if not model_path.exists():
        from src.models.train import train_model
        train_model(profile_name=active_profile)

    logger.info(f"Loading model from: {model_path}")
    model = joblib.load(model_path)

    X_train, X_test, y_train, y_test, _ = process_dataset()
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    metrics = compute_classification_metrics(y_test, y_pred, y_prob)
    latency_ms = measure_inference_latency(model, X_test.to_numpy())
    metrics["latency_ms"] = latency_ms

    # 5-Fold Cross Validation per Senior ML Reviewer feedback
    cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
    metrics["cv_accuracy_mean"] = float(np.mean(cv_scores))
    metrics["cv_accuracy_std"] = float(np.std(cv_scores))

    # Profile-specific target thresholds
    profile_cfg = config.get("model", {}).get("profiles", {}).get(active_profile, {})
    target_acc = profile_cfg.get("target_accuracy", config["evaluation"]["target_accuracy"])
    target_f1 = profile_cfg.get("target_f1", config["evaluation"]["target_f1"])
    target_latency = profile_cfg.get("target_latency_ms", config["evaluation"].get("target_latency_ms", 50.0))

    logger.info(f"Evaluation Results -> Accuracy:    {metrics['accuracy']:.4f} (Target: {target_acc})")
    logger.info(f"Evaluation Results -> F1 Score:    {metrics['f1_score']:.4f} (Target: {target_f1})")
    logger.info(f"Evaluation Results -> CV Accuracy: {metrics['cv_accuracy_mean']:.4f} +/- {metrics['cv_accuracy_std']:.4f}")
    logger.info(f"Evaluation Results -> Latency:     {latency_ms:.2f} ms (Target: <{target_latency} ms)")

    passed = (
        metrics["accuracy"] >= target_acc
        and metrics["f1_score"] >= target_f1
        and latency_ms <= target_latency
    )
    status_str = "PASSED" if passed else "FAILED"
    logger.info(f"Quality Gate Status [{active_profile}]: {status_str}")

    cm_path = root / config["model"]["artifacts_dir"] / config["evaluation"]["confusion_matrix_filename"]
    with open(cm_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "active_profile": active_profile,
                "metrics": metrics,
                "passed_thresholds": passed,
                "thresholds": {
                    "accuracy": target_acc,
                    "f1_score": target_f1,
                    "latency_ms": target_latency,
                },
            },
            f,
            indent=2,
        )

    return passed


if __name__ == "__main__":
    evaluate_model()
