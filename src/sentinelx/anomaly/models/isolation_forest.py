"""Isolation Forest anomaly detection model."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


@dataclass
class AnomalyModelConfig:
    contamination: float = 0.03
    n_estimators: int = 300
    random_state: int = 42
    n_jobs: int = -1


class IsolationForestAnomalyModel:
    """Production-oriented wrapper around IsolationForest."""

    def __init__(
        self,
        config: AnomalyModelConfig | None = None,
    ) -> None:
        self.config = config or AnomalyModelConfig()

        self.model = IsolationForest(
            n_estimators=self.config.n_estimators,
            contamination=self.config.contamination,
            random_state=self.config.random_state,
            n_jobs=self.config.n_jobs,
        )

        self.feature_columns: list[str] = []
        self.is_fitted = False

    def fit(
        self,
        X: pd.DataFrame,
        feature_columns: list[str],
    ) -> "IsolationForestAnomalyModel":
        self.feature_columns = list(feature_columns)

        matrix = (
            X[self.feature_columns]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0.0)
        )

        self.model.fit(matrix)
        self.is_fitted = True

        return self

    def score_samples(
        self,
        X: pd.DataFrame,
    ) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError(
                "Anomaly model must be fitted before scoring."
            )

        matrix = (
            X[self.feature_columns]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0.0)
        )

        # sklearn IsolationForest score_samples:
        # larger values = more normal.
        #
        # Negating gives an anomaly-oriented score:
        # larger values = more anomalous.
        return -self.model.score_samples(matrix)

    def predict(
        self,
        X: pd.DataFrame,
    ) -> np.ndarray:
        if not self.is_fitted:
            raise RuntimeError(
                "Anomaly model must be fitted before prediction."
            )

        matrix = (
            X[self.feature_columns]
            .replace([np.inf, -np.inf], np.nan)
            .fillna(0.0)
        )

        return self.model.predict(matrix)

    def save(self, path: str | Path) -> None:
        if not self.is_fitted:
            raise RuntimeError(
                "Cannot save an unfitted anomaly model."
            )

        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        joblib.dump(self, path)

    @classmethod
    def load(
        cls,
        path: str | Path,
    ) -> "IsolationForestAnomalyModel":
        model = joblib.load(path)

        if not isinstance(model, cls):
            raise TypeError(
                "Artifact is not an IsolationForestAnomalyModel."
            )

        return model
