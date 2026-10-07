"""
Model evaluation against quality thresholds and production criteria.
"""

from pathlib import Path
import json
import joblib
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config
from src.data.preprocess import process_dataset
from src.utils.metrics import compute_classification_metrics


def evaluate_model() -> bool:
    """Evaluates the saved model against predefined performance criteria."""
    config = load_config()
    root = get_project_root()
    model_path = root / config["model"]["artifacts_dir"] / config["model"]["model_filename"]

    if not model_path.exists():
        from src.models.train import train_model
        train_model()

    logger.info(f"Loading model from: {model_path}")
    model = joblib.load(model_path)

    _, X_test, _, y_test, _ = process_dataset()
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)

    metrics = compute_classification_metrics(y_test, y_pred, y_prob)
    target_acc = config["evaluation"]["target_accuracy"]
    target_f1 = config["evaluation"]["target_f1"]

    logger.info(f"Evaluation Results -> Accuracy: {metrics['accuracy']:.4f} (Target: {target_acc})")
    logger.info(f"Evaluation Results -> F1 Score: {metrics['f1_score']:.4f} (Target: {target_f1})")

    passed = metrics["accuracy"] >= target_acc and metrics["f1_score"] >= target_f1
    status_str = "PASSED" if passed else "FAILED"
    logger.info(f"Quality Gate Status: {status_str}")

    cm_path = root / config["model"]["artifacts_dir"] / config["evaluation"]["confusion_matrix_filename"]
    with open(cm_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "metrics": metrics,
                "passed_thresholds": passed,
                "thresholds": {"accuracy": target_acc, "f1_score": target_f1},
            },
            f,
            indent=2,
        )

    return passed


if __name__ == "__main__":
    evaluate_model()
