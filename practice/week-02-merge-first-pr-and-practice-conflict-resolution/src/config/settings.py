"""
Configuration parser and profile resolver for ML project.
Supports multi-profile selection resolving feature branch merge conflicts.
"""

from pathlib import Path
from typing import Any, Dict
import yaml


def get_project_root() -> Path:
    """Returns absolute path to the project root directory."""
    return Path(__file__).resolve().parent.parent.parent


def load_config(config_path: str | Path | None = None) -> Dict[str, Any]:
    """Loads YAML configuration file."""
    if config_path is None:
        config_path = get_project_root() / "configs" / "config.yaml"
    else:
        config_path = Path(config_path)

    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    return config


def get_active_hyperparameters(
    config: Dict[str, Any] | None = None, profile_name: str | None = None
) -> Dict[str, Any]:
    """
    Resolves hyperparameters based on active profile or explicit profile override.
    Demonstrates conflict resolution architecture allowing both regularized and
    lightweight edge configurations to coexist harmoniously.
    """
    if config is None:
        config = load_config()

    profiles = config.get("model", {}).get("profiles", {})
    active = profile_name or config.get("model", {}).get("active_profile", "production_regularized")

    if active in profiles:
        params = profiles[active].copy()
        # Remove non-estimator metadata keys
        params.pop("description", None)
        params.pop("target_accuracy", None)
        params.pop("target_f1", None)
        params.pop("target_latency_ms", None)
        return params

    return config.get("model", {}).get("hyperparameters", {}).copy()
