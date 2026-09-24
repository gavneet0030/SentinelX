import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sentinelx.ml.models import (
    build_logistic_model,
    build_xgboost_model,
)


def make_training_frame():
    rows = []

    for index in range(20):
        rows.append(
            {
                "amount": float(10 + index),
                "log_amount": 0.0,
                "hour": index % 24,
                "day_of_week": index % 7,
                "is_weekend": int(index % 7 >= 5),
                "customer_txn_count_prior": float(index),
                "customer_avg_amount_prior": 10.0,
                "merchant_txn_count_prior": float(index),
                "device_txn_count_prior": float(index),
                "payment_method": "card",
                "channel": "web",
                "country": "IN",
            }
        )

    return pd.DataFrame(rows)


def test_logistic_pipeline_can_fit():
    frame = make_training_frame()

    y = [0, 1] * 10

    model = build_logistic_model()

    model.fit(frame, y)

    probabilities = model.predict_proba(frame)

    assert probabilities.shape == (20, 2)


def test_xgboost_pipeline_can_fit():
    frame = make_training_frame()

    y = [0, 1] * 10

    model = build_xgboost_model()

    model.fit(frame, y)

    probabilities = model.predict_proba(frame)

    assert probabilities.shape == (20, 2)
