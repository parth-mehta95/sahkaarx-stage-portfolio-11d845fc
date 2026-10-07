"""
Baseline ML model architecture and wrapper.
"""

from typing import Any, Dict
from sklearn.ensemble import RandomForestClassifier
from src.utils.logger import logger


def build_model(hyperparameters: Dict[str, Any] | None = None) -> RandomForestClassifier:
    """Builds and initializes the classifier with provided hyperparameters."""
    if hyperparameters is None:
        hyperparameters = {
            "n_estimators": 100,
            "max_depth": 8,
            "min_samples_split": 4,
            "min_samples_leaf": 2,
            "random_state": 42,
            "n_jobs": -1,
        }

    logger.info(f"Initializing RandomForestClassifier with params: {hyperparameters}")
    return RandomForestClassifier(**hyperparameters)
