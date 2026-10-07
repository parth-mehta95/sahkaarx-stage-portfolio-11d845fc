"""
End-to-end Machine Learning Pipeline Runner.
Orchestrates: Ingestion -> Preprocessing -> Model Training -> Evaluation -> Quality Gate.
Supports execution across reconciled profiles ('production_regularized' and 'edge_low_latency').
"""

import sys
from src.utils.logger import logger
from src.data.make_dataset import generate_synthetic_data
from src.data.preprocess import process_dataset
from src.models.train import train_model
from src.models.evaluate import evaluate_model
from src.config.settings import get_project_root, load_config


def run_pipeline(profile_name: str | None = None) -> bool:
    """Executes the full automated ML training and evaluation lifecycle."""
    config = load_config()
    root = get_project_root()
    active_profile = profile_name or config.get("model", {}).get("active_profile", "production_regularized")

    logger.info("==================================================")
    logger.info(f"Starting End-to-End ML Pipeline Execution [{active_profile}]")
    logger.info("==================================================")

    # Step 1: Data Ingestion
    logger.info("[Step 1/4] Checking and preparing raw data...")
    raw_path = root / config["data"]["raw_dir"] / "dataset.csv"
    if not raw_path.exists():
        generate_synthetic_data(
            n_samples=config["data"]["synthetic_samples"],
            n_features=config["data"]["feature_count"],
            random_state=config["data"]["random_state"],
            output_path=raw_path,
        )

    # Step 2: Data Preprocessing
    logger.info("[Step 2/4] Preprocessing dataset and extracting splits...")
    processed_dir = root / config["data"]["processed_dir"]
    process_dataset(raw_path=raw_path, output_dir=processed_dir)

    # Step 3: Model Training
    logger.info(f"[Step 3/4] Fitting model and serializing checkpoints for profile: {active_profile}...")
    model_path = train_model(profile_name=active_profile)
    logger.info(f"Model saved to: {model_path}")

    # Step 4: Quality Gate & Evaluation
    logger.info("[Step 4/4] Evaluating model against production quality gates...")
    passed = evaluate_model(profile_name=active_profile)

    if passed:
        logger.info(f" Pipeline execution completed successfully! Profile '{active_profile}' PASSED all quality gates.")
    else:
        logger.warning(f" Pipeline completed with warnings: Quality gate thresholds for '{active_profile}' were not met.")

    logger.info("==================================================")
    return passed


if __name__ == "__main__":
    profile = sys.argv[1] if len(sys.argv) > 1 else None
    run_pipeline(profile_name=profile)
