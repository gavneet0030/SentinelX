import numpy as np
import pandas as pd

from sentinelx.integration import ml_adapter


class FakePreprocessor:
    feature_names_in_ = np.array([
        "amount",
        "log_amount",
        "hour",
        "day_of_week",
        "is_weekend",
        "customer_txn_count_prior",
        "customer_avg_amount_prior",
        "merchant_txn_count_prior",
        "device_txn_count_prior",
        "payment_method",
        "channel",
        "country",
    ])


class FakeModel:
    named_steps = {"preprocessor": FakePreprocessor()}

    def predict_proba(self, X):
        assert "log_amount" in X.columns
        assert "hour" in X.columns
        assert "customer_txn_count_prior" in X.columns
        assert X["customer_txn_count_prior"].tolist() == [0.0, 1.0, 2.0]
        return np.tile([0.8, 0.2], (len(X), 1))


def test_adapter_engineers_features_before_prediction(tmp_path, monkeypatch):
    raw = pd.DataFrame({
        "transaction_id": ["t1", "t2", "t3"],
        "customer_id": ["c1", "c1", "c1"],
        "merchant_id": ["m1", "m1", "m1"],
        "timestamp": pd.to_datetime([
            "2026-01-01T00:00:00Z",
            "2026-01-01T01:00:00Z",
            "2026-01-01T02:00:00Z",
        ]),
        "amount": [10.0, 20.0, 30.0],
        "currency": ["INR", "INR", "INR"],
        "payment_method": ["card", "card", "card"],
        "channel": ["web", "web", "web"],
        "country": ["IN", "IN", "IN"],
        "device_id": ["d1", "d1", "d1"],
        "ip_address": ["127.0.0.1"] * 3,
        "is_fraud": [0, 1, 0],
    })

    data_path = tmp_path / "data" / "processed" / "transactions.parquet"
    model_path = tmp_path / "models" / "xgboost" / "model.joblib"
    data_path.parent.mkdir(parents=True)
    model_path.parent.mkdir(parents=True)
    data_path.touch()
    model_path.touch()

    monkeypatch.setattr(
        ml_adapter.pd,
        "read_parquet",
        lambda path: raw.copy(),
    )
    monkeypatch.setattr(
        ml_adapter.joblib,
        "load",
        lambda path: FakeModel(),
    )
    monkeypatch.setattr(
        pd.DataFrame,
        "to_parquet",
        lambda self, path, index=False: None,
    )

    result = ml_adapter.MLSignalAdapter(tmp_path).generate_predictions()

    assert result["transaction_id"].tolist() == ["t1", "t2", "t3"]
    assert result["fraud_probability"].tolist() == [0.2, 0.2, 0.2]
    assert result["fraud_prediction"].tolist() == [0, 0, 0]
    assert len(result) == len(raw)
