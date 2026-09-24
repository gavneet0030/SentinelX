from __future__ import annotations

from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = [
    "transaction_id",
    "customer_id",
    "merchant_id",
    "timestamp",
    "amount",
    "currency",
    "payment_method",
    "channel",
    "country",
    "device_id",
    "ip_address",
    "is_fraud",
]


def load_transactions(
    path: str | Path,
) -> pd.DataFrame:

    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(
            f"Transaction file not found: {path}"
        )

    df = pd.read_csv(path)

    missing = [
        column
        for column in REQUIRED_COLUMNS
        if column not in df.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )

    return df
