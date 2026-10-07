"""
Unit tests for data generation, splitting, and preprocessing transforms.
"""

import pandas as pd
from src.data.make_dataset import generate_synthetic_data
from src.data.preprocess import DataPreprocessor, process_dataset


def test_generate_synthetic_data():
    """Verify synthetic data generator output shape and target column."""
    df = generate_synthetic_data(n_samples=100, n_features=8, n_classes=2, random_state=42)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (100, 9)
    assert "target" in df.columns
    assert set(df["target"].unique()) == {0, 1}


def test_preprocessor_split_and_scale():
    """Verify preprocessor correctly splits, transforms, and preserves dimensions."""
    df = generate_synthetic_data(n_samples=200, n_features=6, random_state=42)
    preprocessor = DataPreprocessor(target_column="target", test_size=0.25, random_state=42)

    X, y = preprocessor.split_features_target(df)
    assert X.shape == (200, 6)
    assert len(y) == 200

    X_train, X_test, y_train, y_test = preprocessor.train_test_split(X, y)
    assert len(X_train) == 150
    assert len(X_test) == 50

    X_train_scaled = preprocessor.fit_transform(X_train)
    X_test_scaled = preprocessor.transform(X_test)

    assert X_train_scaled.shape == (150, 6)
    assert X_test_scaled.shape == (50, 6)
    # Scaled training data mean should be close to 0
    assert abs(X_train_scaled.mean().mean()) < 1e-5


def test_process_dataset_end_to_end():
    """Verify high-level process_dataset function returns all expected objects."""
    X_train, X_test, y_train, y_test, preprocessor = process_dataset()
    assert len(X_train) > 0
    assert len(X_test) > 0
    assert len(y_train) == len(X_train)
    assert len(y_test) == len(X_test)
    assert isinstance(preprocessor, DataPreprocessor)
