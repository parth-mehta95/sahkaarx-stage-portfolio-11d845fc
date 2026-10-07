"""
Unit tests for data generation and preprocessing modules.
"""

import pytest
import pandas as pd
import numpy as np
from src.data.make_dataset import generate_synthetic_data
from src.data.preprocess import DataPreprocessor


def test_generate_synthetic_data():
    """Verify synthetic data generator produces correct shape and columns."""
    n_samples = 150
    n_features = 8
    df = generate_synthetic_data(n_samples=n_samples, n_features=n_features, random_state=42)

    assert isinstance(df, pd.DataFrame)
    assert df.shape == (n_samples, n_features + 1)
    assert "target" in df.columns
    assert set(df["target"].unique()).issubset({0, 1})
    assert df.isnull().sum().sum() == 0


def test_data_preprocessor_split():
    """Verify data preprocessor splits correctly and scales features."""
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

    # Scaled training data should have zero mean and unit variance approximately
    np.testing.assert_allclose(X_train_scaled.mean(axis=0), np.zeros(6), atol=1e-1)
    np.testing.assert_allclose(X_train_scaled.std(axis=0), np.ones(6), atol=1e-1)
