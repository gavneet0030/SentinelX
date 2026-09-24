import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sentinelx.ml.dataset import time_based_split
from sentinelx.ml.features import (
    CATEGORICAL_FEATURES,
    NUMERIC_FEATURES,
    build_features,
)


def test_feature_columns():
    frame = pd.DataFrame(
        {
            "transaction_id": ["a", "b", "c"],
            "customer_id": ["c1", "c1", "c2"],
            "merchant_id": ["m1", "m1", "m2"],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T01:00:00Z",
                    "2026-01-02T01:00:00Z",
                ]
            ),
            "amount": [10.0, 20.0, 50.0],
            "payment_method": [
                "card",
                "card",
                "wallet",
            ],
            "channel": [
                "web",
                "mobile",
                "web",
            ],
            "country": [
                "IN",
                "IN",
                "US",
            ],
            "device_id": [
                "d1",
                "d1",
                "d2",
            ],
            "is_fraud": [
                0,
                1,
                0,
            ],
        }
    )

    result = build_features(frame)

    for column in (
        NUMERIC_FEATURES
        + CATEGORICAL_FEATURES
    ):
        assert column in result.columns


def test_historical_customer_feature_has_no_current_transaction_leakage():
    frame = pd.DataFrame(
        {
            "transaction_id": ["a", "b"],
            "customer_id": ["c1", "c1"],
            "merchant_id": ["m1", "m1"],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01T00:00:00Z",
                    "2026-01-02T00:00:00Z",
                ]
            ),
            "amount": [100.0, 900.0],
            "payment_method": [
                "card",
                "card",
            ],
            "channel": [
                "web",
                "web",
            ],
            "country": [
                "IN",
                "IN",
            ],
            "device_id": [
                "d1",
                "d1",
            ],
            "is_fraud": [
                0,
                1,
            ],
        }
    )

    result = build_features(frame)

    assert result.loc[0, "customer_txn_count_prior"] == 0
    assert result.loc[1, "customer_txn_count_prior"] == 1

    assert result.loc[
        0,
        "customer_avg_amount_prior"
    ] == 0

    assert result.loc[
        1,
        "customer_avg_amount_prior"
    ] == 100


def test_time_split_preserves_order():
    frame = pd.DataFrame(
        {
            "transaction_id": [
                "a",
                "b",
                "c",
                "d",
                "e",
                "f",
                "g",
                "h",
                "i",
                "j",
            ],
            "timestamp": pd.date_range(
                "2026-01-01",
                periods=10,
                freq="h",
                tz="UTC",
            ),
            "is_fraud": [0] * 10,
        }
    )

    train, validation, test = time_based_split(
        frame,
        train_ratio=0.7,
        validation_ratio=0.15,
    )

    assert len(train) == 7
    assert len(validation) == 1
    assert len(test) == 2

    assert (
        train["timestamp"].max()
        < validation["timestamp"].min()
    )

    assert (
        validation["timestamp"].max()
        < test["timestamp"].min()
    )
