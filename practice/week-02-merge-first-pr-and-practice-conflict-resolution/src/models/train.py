"""
Model training script with hyperparameter logging and artifact serialization.
Supports multi-profile execution reconciling Branch A & Branch B contributions.
"""

from pathlib import Path
import json
import joblib
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config, get_active_hyperparameters
from src.data.preprocess import process_dataset
from src.models.baseline_model import build_model
from src.utils.metrics import compute_classification_metrics, measure_inference_latency


def train_model(profile_name: str | None = None) -> Path:
    """Executes model training pipeline, logs performance, and saves model."""
    config = load_config()
    root = get_project_root()
    active_profile = profile_name or config.get("model", {}).get("active_profile", "production_regularized")

    logger.info(f"Starting model training pipeline [Active Profile: {active_profile}]...")
    X_train, X_test, y_train, y_test, _ = process_dataset()

    hyperparams = get_active_hyperparameters(config, profile_name=active_profile)
    model = build_model(hyperparams)
    model.fit(X_train, y_train)

    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    test_probs = model.predict_proba(X_test)

    train_metrics = compute_classification_metrics(y_train, train_preds)
    test_metrics = compute_classification_metrics(y_test, test_preds, test_probs)
    latency_ms = measure_inference_latency(model, X_test.to_numpy())
    test_metrics["latency_ms"] = latency_ms

    logger.info(f"Train Accuracy: {train_metrics['accuracy']:.4f}")
    logger.info(f"Test Accuracy:  {test_metrics['accuracy']:.4f}")
    logger.info(f"Test F1 Score:  {test_metrics['f1_score']:.4f}")
    logger.info(f"Avg Latency:    {latency_ms:.2f} ms")

    artifacts_dir = root / config["model"]["artifacts_dir"]
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    model_path = artifacts_dir / config["model"]["model_filename"]
    joblib.dump(model, model_path)
    logger.info(f"Model saved successfully to: {model_path}")

    metrics_path = artifacts_dir / config["model"]["metrics_filename"]
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "active_profile": active_profile,
                "train_metrics": train_metrics,
                "test_metrics": test_metrics,
                "model_parameters": hyperparams,
            },
            f,
            indent=2,
        )
    logger.info(f"Metrics saved to: {metrics_path}")

    return model_path


if __name__ == "__main__":
    train_model()
