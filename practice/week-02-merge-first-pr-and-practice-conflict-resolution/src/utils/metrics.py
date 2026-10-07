"""
Model performance evaluation metrics calculations.
Enhanced per PR #1 team review feedback to include latency benchmarking and detailed diagnostics.
"""

from typing import Dict, Any
import time
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
)


def compute_classification_metrics(
    y_true: np.ndarray, y_pred: np.ndarray, y_prob: np.ndarray | None = None
) -> Dict[str, Any]:
    """Calculates classification evaluation metrics."""
    metrics = {
        "accuracy": float(accuracy_score(y_true, y_pred)),
        "precision": float(precision_score(y_true, y_pred, average="weighted", zero_division=0)),
        "recall": float(recall_score(y_true, y_pred, average="weighted", zero_division=0)),
        "f1_score": float(f1_score(y_true, y_pred, average="weighted", zero_division=0)),
    }

    if y_prob is not None:
        try:
            if y_prob.ndim == 2 and y_prob.shape[1] == 2:
                metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob[:, 1]))
            elif y_prob.ndim == 1:
                metrics["roc_auc"] = float(roc_auc_score(y_true, y_prob))
        except Exception:
            metrics["roc_auc"] = None

    cm = confusion_matrix(y_true, y_pred)
    metrics["confusion_matrix"] = cm.tolist()

    return metrics


def measure_inference_latency(model: Any, X_sample: np.ndarray, repetitions: int = 50) -> float:
    """
    Measures average inference latency in milliseconds.
    Addresses latency verification required by edge inference squad.
    """
    latencies = []
    # Warmup
    _ = model.predict(X_sample[:1])

    for _ in range(repetitions):
        start = time.perf_counter()
        _ = model.predict(X_sample)
        latencies.append((time.perf_counter() - start) * 1000.0)

    return float(np.mean(latencies))
