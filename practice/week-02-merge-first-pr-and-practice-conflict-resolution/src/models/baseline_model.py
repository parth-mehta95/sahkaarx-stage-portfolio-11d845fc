"""
Baseline and enhanced ML model architecture with input validation.
Addresses PR #1 review feedback (parameter bounds checking) and synthesizes
conflicting feature branch enhancements (regularization & efficiency).
"""

from typing import Any, Dict
from sklearn.ensemble import RandomForestClassifier
from src.utils.logger import logger


def validate_hyperparameters(params: Dict[str, Any]) -> None:
    """
    Validates hyperparameter ranges to prevent misconfigured model runs.
    Added in response to Tech Lead review on PR #1.
    """
    if "n_estimators" in params and params["n_estimators"] <= 0:
        raise ValueError(f"n_estimators must be positive, got {params['n_estimators']}")

    if "max_depth" in params and params["max_depth"] is not None and params["max_depth"] <= 0:
        raise ValueError(f"max_depth must be positive or None, got {params['max_depth']}")

    if "min_samples_split" in params and params["min_samples_split"] < 2:
        raise ValueError(f"min_samples_split must be >= 2, got {params['min_samples_split']}")

    valid_criteria = {"gini", "entropy", "log_loss"}
    if "criterion" in params and params["criterion"] not in valid_criteria:
        raise ValueError(f"criterion must be one of {valid_criteria}, got {params['criterion']}")


def build_model(hyperparameters: Dict[str, Any] | None = None) -> RandomForestClassifier:
    """
    Builds and initializes the classifier with provided hyperparameters.
    Harmonizes Branch A (regularization) and Branch B (efficiency parameters).
    """
    if hyperparameters is None:
        # Reconciled default parameters balancing capacity and speed
        hyperparameters = {
            "n_estimators": 120,
            "max_depth": 10,
            "min_samples_split": 4,
            "min_samples_leaf": 2,
            "max_features": "sqrt",
            "criterion": "entropy",
            "class_weight": "balanced",
            "random_state": 42,
            "n_jobs": -1,
        }

    # Validate parameters per PR review criteria
    validate_hyperparameters(hyperparameters)

    logger.info(f"Initializing RandomForestClassifier with validated parameters: {hyperparameters}")
    return RandomForestClassifier(**hyperparameters)
