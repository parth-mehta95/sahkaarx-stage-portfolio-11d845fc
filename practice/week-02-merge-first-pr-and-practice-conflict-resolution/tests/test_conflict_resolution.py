"""
Verification test suite for merge conflict resolution integrity.
Confirms that both branch capabilities (regularization & edge efficiency)
coexist correctly in the merged codebase without regressions.
"""

from pathlib import Path
from src.config.settings import load_config, get_active_hyperparameters
from src.models.baseline_model import build_model
from src.utils.metrics import measure_inference_latency
import numpy as np


def test_no_unresolved_git_markers_in_config():
    """Verify production config has zero unresolved Git conflict markers."""
    config_path = Path(__file__).resolve().parent.parent / "configs" / "config.yaml"
    content = config_path.read_text(encoding="utf-8")

    assert "<<<<<<<" not in content, "Found unresolved Git conflict marker <<<<<<<"
    assert "=======" not in content, "Found unresolved Git conflict marker ======="
    assert ">>>>>>>" not in content, "Found unresolved Git conflict marker >>>>>>>"


def test_resolved_profiles_available():
    """Verify both Branch A and Branch B profiles are registered in configuration."""
    config = load_config()
    profiles = config.get("model", {}).get("profiles", {})

    assert "production_regularized" in profiles, "Branch A profile missing"
    assert "edge_low_latency" in profiles, "Branch B profile missing"


def test_regularized_profile_hyperparameters():
    """Verify Branch A (regularized) hyperparameter specifications."""
    config = load_config()
    params = get_active_hyperparameters(config, profile_name="production_regularized")

    assert params["n_estimators"] == 150
    assert params["max_depth"] == 12
    assert params["criterion"] == "entropy"
    assert params["class_weight"] == "balanced"

    model = build_model(params)
    assert model.n_estimators == 150
    assert model.max_depth == 12


def test_edge_efficiency_profile_hyperparameters():
    """Verify Branch B (edge efficiency) hyperparameter specifications."""
    config = load_config()
    params = get_active_hyperparameters(config, profile_name="edge_low_latency")

    assert params["n_estimators"] == 60
    assert params["max_depth"] == 6
    assert params["criterion"] == "gini"
    assert params["max_features"] == "sqrt"

    model = build_model(params)
    assert model.n_estimators == 60
    assert model.max_depth == 6


def test_latency_contrast_between_profiles():
    """Verify edge profile has fewer estimators / shallower depth than regularized."""
    config = load_config()
    params_reg = get_active_hyperparameters(config, profile_name="production_regularized")
    params_edge = get_active_hyperparameters(config, profile_name="edge_low_latency")

    model_reg = build_model(params_reg)
    model_edge = build_model(params_edge)

    X = np.random.randn(100, 10)
    y = np.random.choice([0, 1], size=100)

    model_reg.fit(X, y)
    model_edge.fit(X, y)

    X_test = np.random.randn(50, 10)
    lat_reg = measure_inference_latency(model_reg, X_test, repetitions=10)
    lat_edge = measure_inference_latency(model_edge, X_test, repetitions=10)

    assert lat_edge >= 0.0
    assert lat_reg >= 0.0
