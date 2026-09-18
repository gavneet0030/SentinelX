"""
Unsupervised anomaly detection.
"""

from sklearn.ensemble import IsolationForest
import pandas as pd


class AnomalyDetector:

    def __init__(
        self,
        contamination: float = 0.01,
        random_state: int = 42,
    ):
        self.model = IsolationForest(
            contamination=contamination,
            random_state=random_state,
        )

    def fit(self, X):
        self.model.fit(X)
        return self

    def predict(self, X):
        return self.model.predict(X)

    def score_samples(self, X):
        return self.model.score_samples(X)
