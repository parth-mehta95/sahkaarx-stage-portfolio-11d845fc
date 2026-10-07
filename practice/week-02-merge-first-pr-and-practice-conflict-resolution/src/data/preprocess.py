"""
Data preprocessing, feature engineering, and train/test splitting.
"""

from pathlib import Path
from typing import Tuple
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config


class DataPreprocessor:
    """Preprocesses features and handles dataset splitting."""

    def __init__(self, target_column: str = "target", test_size: float = 0.2, random_state: int = 42):
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.scaler = StandardScaler()

    def split_features_target(self, df: pd.DataFrame) -> Tuple[pd.DataFrame, pd.Series]:
        """Separates features X and target y."""
        X = df.drop(columns=[self.target_column])
        y = df[self.target_column]
        return X, y

    def train_test_split(
        self, X: pd.DataFrame, y: pd.Series
    ) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
        """Splits data into train and test sets."""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )
        logger.info(
            f"Train/Test split completed: Train={len(X_train)} samples, Test={len(X_test)} samples"
        )
        return X_train, X_test, y_train, y_test

    def fit_transform(self, X_train: pd.DataFrame) -> pd.DataFrame:
        """Fits scaler on training data and transforms it."""
        scaled = self.scaler.fit_transform(X_train)
        return pd.DataFrame(scaled, columns=X_train.columns, index=X_train.index)

    def transform(self, X_test: pd.DataFrame) -> pd.DataFrame:
        """Transforms test data using fitted scaler."""
        scaled = self.scaler.transform(X_test)
        return pd.DataFrame(scaled, columns=X_test.columns, index=X_test.index)


def process_dataset(
    raw_path: str | Path | None = None,
    output_dir: str | Path | None = None,
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series, DataPreprocessor]:
    """Complete preprocessing pipeline execution."""
    config = load_config()
    root = get_project_root()

    if raw_path is None:
        raw_path = root / config["data"]["raw_dir"] / "dataset.csv"
    else:
        raw_path = Path(raw_path)

    if not raw_path.exists():
        from src.data.make_dataset import generate_synthetic_data
        generate_synthetic_data(output_path=raw_path)

    df = pd.read_csv(raw_path)
    preprocessor = DataPreprocessor(
        target_column=config["data"]["target_column"],
        test_size=config["data"]["test_size"],
        random_state=config["data"]["random_state"],
    )

    X, y = preprocessor.split_features_target(df)
    X_train, X_test, y_train, y_test = preprocessor.train_test_split(X, y)

    X_train_scaled = preprocessor.fit_transform(X_train)
    X_test_scaled = preprocessor.transform(X_test)

    if output_dir is not None:
        out_dir = Path(output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        X_train_scaled.to_parquet(out_dir / "X_train.parquet")
        X_test_scaled.to_parquet(out_dir / "X_test.parquet")
        y_train.to_frame().to_parquet(out_dir / "y_train.parquet")
        y_test.to_frame().to_parquet(out_dir / "y_test.parquet")
        logger.info(f"Saved processed datasets to: {out_dir}")

    return X_train_scaled, X_test_scaled, y_train, y_test, preprocessor
