"""
Configuration parser and environment loader.
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
