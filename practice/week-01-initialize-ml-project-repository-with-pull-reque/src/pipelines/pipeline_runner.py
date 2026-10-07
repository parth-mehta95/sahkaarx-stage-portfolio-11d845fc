"""
End-to-end Machine Learning Pipeline Runner.
Orchestrates: Ingestion -> Preprocessing -> Model Training -> Evaluation -> Quality Gate.
"""

from src.utils.logger import logger
from src.data.make_dataset import generate_synthetic_data
from src.data.preprocess import process_dataset
from src.models.train import train_model
from src.models.evaluate import evaluate_model
from src.config.settings import get_project_root, load_config


def run_pipeline() -> bool:
    """Executes the full automated ML training and evaluation lifecycle."""
    logger.info("==================================================")
    logger.info("Starting End-to-End ML Pipeline Execution")
    logger.info("==================================================")

    config = load_config()
    root = get_project_root()

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
    logger.info("[Step 3/4] Fitting model and serializing checkpoints...")
    model_path = train_model()
    logger.info(f"Model saved to: {model_path}")

    # Step 4: Quality Gate & Evaluation
    logger.info("[Step 4/4] Evaluating model against production quality gates...")
    passed = evaluate_model()

    if passed:
        logger.info(" Pipeline execution completed successfully! Model PASSED all quality gates.")
    else:
        logger.warning(" Pipeline completed with warnings: Quality gate thresholds were not met.")

    logger.info("==================================================")
    return passed


if __name__ == "__main__":
    run_pipeline()
