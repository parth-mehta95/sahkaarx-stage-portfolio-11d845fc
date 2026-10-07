"""
Integration tests for end-to-end ML training and evaluation pipeline.
"""

from src.pipelines.pipeline_runner import run_pipeline


def test_pipeline_execution_default():
    """Verify end-to-end pipeline executes and passes quality gates."""
    result = run_pipeline()
    assert result is True


def test_pipeline_execution_edge_profile():
    """Verify end-to-end pipeline executes successfully for edge_low_latency profile."""
    result = run_pipeline(profile_name="edge_low_latency")
    assert result is True
