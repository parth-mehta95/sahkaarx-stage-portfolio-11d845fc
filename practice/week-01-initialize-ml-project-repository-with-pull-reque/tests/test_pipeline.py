"""
Integration tests for end-to-end ML pipeline orchestration.
"""

import pytest
from pathlib import Path
from src.config.settings import load_config, get_project_root
from src.pipelines.pipeline_runner import run_pipeline


def test_pipeline_execution():
    """Verify that end-to-end pipeline runs and generates expected artifacts."""
    config = load_config()
    root = get_project_root()

    success = run_pipeline()
    assert success is True

    # Validate output artifacts exist
    artifacts_dir = root / config["model"]["artifacts_dir"]
    model_file = artifacts_dir / config["model"]["model_filename"]
    metrics_file = artifacts_dir / config["model"]["metrics_filename"]

    assert model_file.exists()
    assert metrics_file.exists()
