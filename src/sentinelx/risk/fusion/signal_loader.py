"""
SentinelX unified signal loader.
"""

from pathlib import Path
import pandas as pd


class SignalLoader:

    def __init__(self, root):
        self.root = Path(root)

    def load_transactions(self):

        return pd.read_parquet(
            self.root /
            "data" /
            "processed" /
            "transactions.parquet"
        )

    def load_ml(self):

        return pd.read_parquet(
            self.root /
            "reports" /
            "ml" /
            "fraud_predictions.parquet"
        )

    def load_behavioral(self):

        return pd.read_parquet(
            self.root /
            "reports" /
            "behavior" /
            "behavioral_signals.parquet"
        )

    def load_anomaly(self):

        return pd.read_parquet(
            self.root /
            "reports" /
            "anomaly" /
            "anomaly_scores.parquet"
        )

    def merge_all_signals(self):

        transactions = self.load_transactions()
        ml = self.load_ml()
        behavioral = self.load_behavioral()
        anomaly = self.load_anomaly()

        result = transactions[
            ["transaction_id"]
        ].copy()

        result = result.merge(
            ml,
            on="transaction_id",
            how="left"
        )

        result = result.merge(
            behavioral,
            on="transaction_id",
            how="left"
        )

        anomaly_columns = [
            "transaction_id",
            "anomaly_score",
            "anomaly_decision"
        ]

        result = result.merge(
            anomaly[anomaly_columns],
            on="transaction_id",
            how="left"
        )

        numeric_columns = [
            "fraud_probability",
            "behavioral_risk",
            "anomaly_score"
        ]

        for column in numeric_columns:

            result[column] = (
                pd.to_numeric(
                    result[column],
                    errors="coerce"
                )
                .fillna(0)
            )

        return result
