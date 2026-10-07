"""
Unit tests for model architecture, hyperparameter validation, and evaluation metrics.
"""

import numpy as np
import pytest
from src.models.baseline_model import build_model, validate_hyperparameters
from src.utils.metrics import compute_classification_metrics, measure_inference_latency


def test_build_model_default():
    """Verify default model initialization."""
    model = build_model()
    assert model.n_estimators == 120
    assert model.max_depth == 10
    assert model.random_state == 42


def test_validate_hyperparameters_valid():
    """Verify valid hyperparameters pass validation."""
    valid_params = {
        "n_estimators": 50,
        "max_depth": 5,
        "min_samples_split": 2,
        "criterion": "gini",
    }
    validate_hyperparameters(valid_params)  # Should not raise


def test_validate_hyperparameters_invalid():
    """Verify invalid hyperparameters raise proper ValueError."""
    with pytest.raises(ValueError, match="n_estimators must be positive"):
        validate_hyperparameters({"n_estimators": 0})

    with pytest.raises(ValueError, match="max_depth must be positive"):
        validate_hyperparameters({"max_depth": -1})

    with pytest.raises(ValueError, match="criterion must be one of"):
        validate_hyperparameters({"criterion": "invalid_criterion"})


def test_model_fit_predict():
    """Verify model fits data and generates valid predictions and probabilities."""
    model = build_model({"n_estimators": 10, "max_depth": 3, "random_state": 42})
    X = np.random.randn(50, 5)
    y = np.random.choice([0, 1], size=50)

    model.fit(X, y)
    preds = model.predict(X)
    probs = model.predict_proba(X)

    assert len(preds) == 50
    assert probs.shape == (50, 2)
    assert np.all((probs >= 0.0) & (probs <= 1.0))


def test_measure_inference_latency():
    """Verify latency benchmark returns positive float in milliseconds."""
    model = build_model({"n_estimators": 10, "max_depth": 3, "random_state": 42})
    X = np.random.randn(20, 5)
    y = np.random.choice([0, 1], size=20)
    model.fit(X, y)

    latency = measure_inference_latency(model, X, repetitions=5)
    assert isinstance(latency, float)
    assert latency > 0.0


def test_compute_classification_metrics():
    """Verify metrics calculation logic."""
    y_true = np.array([0, 1, 0, 1, 1, 0])
    y_pred = np.array([0, 1, 0, 1, 0, 0])

    metrics = compute_classification_metrics(y_true, y_pred)
    assert "accuracy" in metrics
    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1_score" in metrics
    assert "confusion_matrix" in metrics
    assert 0.0 <= metrics["accuracy"] <= 1.0
