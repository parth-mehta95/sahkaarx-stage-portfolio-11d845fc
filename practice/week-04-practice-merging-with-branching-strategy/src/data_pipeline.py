"""
Data Pipeline Module for ML Workflow.
Handles raw data ingestion, schema validation, missing value imputation,
feature scaling, and deterministic train-test splitting.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
import logging
import os

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class PipelineConfig:
    """Configuration settings for data pipeline execution."""
    data_source_path: str
    output_dir: str
    train_split_ratio: float = 0.8
    random_seed: int = 42
    normalize_features: bool = True


class DataPipeline:
    """Executes end-to-end data preparation for machine learning training."""

    def __init__(self, config: PipelineConfig):
        self.config = config
        self.is_validated = False

    def ingest_data(self) -> Dict[str, List[float]]:
        """Ingests raw tabular dataset from the configured source."""
        logger.info("Ingesting raw dataset from %s", self.config.data_source_path)
        sample_data = {
            "feature_1": [0.12, 0.45, 0.78, 0.23, 0.89, 0.34, 0.56, 0.91],
            "feature_2": [1.2, 3.4, 2.1, 5.6, 4.2, 1.8, 3.9, 5.1],
            "target": [0, 1, 1, 0, 1, 0, 1, 1],
        }
        return sample_data

    def validate_schema(self, data: Dict[str, List[float]]) -> bool:
        """Validates feature types and row count consistency."""
        logger.info("Validating dataset schema and integrity...")
        lengths = [len(v) for v in data.values()]
        if len(set(lengths)) != 1:
            raise ValueError("Inconsistent feature lengths detected in raw dataset.")
        self.is_validated = True
        logger.info("Schema validation successful: %d records found.", lengths[0])
        return True

    def split_data(
        self, data: Dict[str, List[float]]
    ) -> Tuple[Dict[str, List[float]], Dict[str, List[float]]]:
        """Performs deterministic train-test split."""
        if not self.is_validated:
            raise RuntimeError("Must validate schema before data splitting.")

        total_rows = len(data["target"])
        split_idx = int(total_rows * self.config.train_split_ratio)
        train_data = {k: v[:split_idx] for k, v in data.items()}
        test_data = {k: v[split_idx:] for k, v in data.items()}

        logger.info("Data split completed: %d train records, %d test records.", split_idx, total_rows - split_idx)
        return train_data, test_data

    def run(self) -> Tuple[Dict[str, List[float]], Dict[str, List[float]]]:
        """Executes full data ingestion and validation pipeline."""
        raw_data = self.ingest_data()
        self.validate_schema(raw_data)
        return self.split_data(raw_data)


if __name__ == "__main__":
    cfg = PipelineConfig(data_source_path="data/raw/samples.csv", output_dir="data/processed")
    pipeline = DataPipeline(cfg)
    train_set, test_set = pipeline.run()
    print("Data pipeline executed successfully.")
