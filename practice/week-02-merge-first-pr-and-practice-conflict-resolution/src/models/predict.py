"""
Inference prediction engine for single and batch samples.
"""

from pathlib import Path
from typing import Dict, Any
import numpy as np
import pandas as pd
import joblib
from src.utils.logger import logger
from src.config.settings import get_project_root, load_config


class Predictor:
    """Loads trained model checkpoint and performs scoring."""

    def __init__(self, model_path: str | Path | None = None):
        config = load_config()
        root = get_project_root()
        if model_path is None:
            self.model_path = root / config["model"]["artifacts_dir"] / config["model"]["model_filename"]
        else:
            self.model_path = Path(model_path)

        if not self.model_path.exists():
            from src.models.train import train_model
            self.model_path = train_model()

        logger.info(f"Loading inference model checkpoint from: {self.model_path}")
        self.model = joblib.load(self.model_path)

    def predict(self, features: np.ndarray | pd.DataFrame) -> Dict[str, Any]:
        """Runs predictions on input features."""
        predictions = self.model.predict(features)
        probabilities = self.model.predict_proba(features)

        return {
            "predictions": predictions.tolist(),
            "probabilities": probabilities.tolist(),
            "count": len(predictions),
        }


if __name__ == "__main__":
    predictor = Predictor()
    dummy_input = np.random.randn(2, 10)
    result = predictor.predict(dummy_input)
    print("Inference Result:", result)
