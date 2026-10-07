"""
Model training script with hyperparameter logging and artifact serialization.
"""

from pathlib import Path
import json
import joblib
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config
from src.data.preprocess import process_dataset
from src.models.baseline_model import build_model
from src.utils.metrics import compute_classification_metrics


def train_model() -> Path:
    """Executes model training pipeline, logs performance, and saves model."""
    config = load_config()
    root = get_project_root()

    logger.info("Starting model training pipeline...")
    X_train, X_test, y_train, y_test, _ = process_dataset()

    model = build_model(config["model"]["hyperparameters"])
    model.fit(X_train, y_train)

    train_preds = model.predict(X_train)
    test_preds = model.predict(X_test)
    test_probs = model.predict_proba(X_test)

    train_metrics = compute_classification_metrics(y_train, train_preds)
    test_metrics = compute_classification_metrics(y_test, test_preds, test_probs)

    logger.info(f"Train Accuracy: {train_metrics['accuracy']:.4f}")
    logger.info(f"Test Accuracy:  {test_metrics['accuracy']:.4f}")
    logger.info(f"Test F1 Score:  {test_metrics['f1_score']:.4f}")

    artifacts_dir = root / config["model"]["artifacts_dir"]
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    model_path = artifacts_dir / config["model"]["model_filename"]
    joblib.dump(model, model_path)
    logger.info(f"Model saved successfully to: {model_path}")

    metrics_path = artifacts_dir / config["model"]["metrics_filename"]
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "train_metrics": train_metrics,
                "test_metrics": test_metrics,
                "model_parameters": config["model"]["hyperparameters"],
            },
            f,
            indent=2,
        )
    logger.info(f"Metrics saved to: {metrics_path}")

    return model_path


if __name__ == "__main__":
    train_model()
