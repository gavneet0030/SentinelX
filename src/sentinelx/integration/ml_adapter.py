from pathlib import Path

import joblib
import numpy as np
import pandas as pd

from sentinelx.ml.features import build_features


class MLSignalAdapter:
    """Generate fraud signals using the training feature pipeline."""

    def __init__(self, root):
        self.root = Path(root)

    def generate_predictions(self):
        data_path = (
            self.root / "data" / "processed" / "transactions.parquet"
        )
        model_path = (
            self.root / "models" / "xgboost" / "model.joblib"
        )
        output_path = (
            self.root / "reports" / "ml" / "fraud_predictions.parquet"
        )

        if not data_path.is_file():
            raise FileNotFoundError(f"Transaction dataset not found: {data_path}")
        if not model_path.is_file():
            raise FileNotFoundError(f"Trained XGBoost model not found: {model_path}")

        raw = pd.read_parquet(data_path)

        if "transaction_id" not in raw.columns:
            raise ValueError("Dataset is missing transaction_id.")
        if raw["transaction_id"].isna().any():
            raise ValueError("transaction_id contains null values.")
        if raw["transaction_id"].duplicated().any():
            raise ValueError("transaction_id must be unique.")

        model = joblib.load(model_path)

        preprocessor = getattr(model, "named_steps", {}).get("preprocessor")
        required = getattr(preprocessor, "feature_names_in_", None)

        if required is None:
            required = getattr(model, "feature_names_in_", None)

        if required is None:
            raise ValueError(
                "Cannot determine model input features; refusing unsafe inference."
            )

        required = list(required)
        featured = build_features(raw)

        missing = [column for column in required if column not in featured.columns]
        if missing:
            raise ValueError(
                f"Engineered dataset is missing required model features: {missing}"
            )

        X = featured[required].copy()
        probabilities = np.asarray(model.predict_proba(X))[:, 1]

        if len(probabilities) != len(featured):
            raise ValueError("Model returned an unexpected number of predictions.")
        if not np.isfinite(probabilities).all():
            raise ValueError("Model returned non-finite fraud probabilities.")
        if ((probabilities < 0) | (probabilities > 1)).any():
            raise ValueError("Fraud probabilities must be between 0 and 1.")

        result = pd.DataFrame({
            "transaction_id": featured["transaction_id"].to_numpy(),
            "fraud_probability": probabilities,
            "fraud_prediction": (probabilities >= 0.5).astype(int),
            "model_version": "baseline_xgboost_v1",
        })

        output_path.parent.mkdir(parents=True, exist_ok=True)
        result.to_parquet(output_path, index=False)

        print(f"ML predictions saved: {len(result):,} rows -> {output_path}")
        return result
