"""
Dataset generation and ingestion module.
"""

from pathlib import Path
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config


def generate_synthetic_data(
    n_samples: int = 1000,
    n_features: int = 10,
    n_classes: int = 2,
    random_state: int = 42,
    output_path: str | Path | None = None,
) -> pd.DataFrame:
    """Generates synthetic tabular dataset for training and testing."""
    logger.info(f"Generating synthetic dataset: {n_samples} samples, {n_features} features")

    X, y = make_classification(
        n_samples=n_samples,
        n_features=n_features,
        n_informative=int(n_features * 0.7),
        n_redundant=int(n_features * 0.2),
        n_classes=n_classes,
        random_state=random_state,
    )

    feature_cols = [f"feature_{i+1}" for i in range(n_features)]
    df = pd.DataFrame(X, columns=feature_cols)
    df["target"] = y

    if output_path is not None:
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_path, index=False)
        logger.info(f"Saved raw dataset to: {out_path}")

    return df


if __name__ == "__main__":
    config = load_config()
    root = get_project_root()
    raw_path = root / config["data"]["raw_dir"] / "dataset.csv"
    generate_synthetic_data(
        n_samples=config["data"]["synthetic_samples"],
        n_features=config["data"]["feature_count"],
        random_state=config["data"]["random_state"],
        output_path=raw_path,
    )
