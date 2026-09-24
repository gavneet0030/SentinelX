from __future__ import annotations

import numpy as np
import pandas as pd


CATEGORICAL_FEATURES = [
    "payment_method",
    "channel",
    "country",
]

NUMERIC_FEATURES = [
    "amount",
    "log_amount",
    "hour",
    "day_of_week",
    "is_weekend",
    "customer_txn_count_prior",
    "customer_avg_amount_prior",
    "merchant_txn_count_prior",
    "device_txn_count_prior",
]

TARGET_COLUMN = "is_fraud"


def get_feature_columns() -> tuple[list[str], list[str]]:
    """Return numeric and categorical feature definitions."""
    return NUMERIC_FEATURES.copy(), CATEGORICAL_FEATURES.copy()


def build_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Build transaction-level and historical behavioral features.

    Historical features are calculated only from transactions that
    occurred before the current transaction. This prevents future
    information from leaking into the current row.
    """

    required = {
        "transaction_id",
        "customer_id",
        "merchant_id",
        "timestamp",
        "amount",
        "payment_method",
        "channel",
        "country",
        "device_id",
        TARGET_COLUMN,
    }

    missing = required.difference(df.columns)

    if missing:
        raise ValueError(
            f"Missing required columns: {sorted(missing)}"
        )

    result = df.copy()

    result["timestamp"] = pd.to_datetime(
        result["timestamp"],
        utc=True,
        errors="raise",
    )

    result["amount"] = pd.to_numeric(
        result["amount"],
        errors="raise",
    )

    result = result.sort_values(
        ["timestamp", "transaction_id"]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Transaction-local features
    # --------------------------------------------------------

    result["log_amount"] = np.log1p(
        result["amount"].astype(float)
    )

    result["hour"] = result["timestamp"].dt.hour

    result["day_of_week"] = result["timestamp"].dt.dayofweek

    result["is_weekend"] = (
        result["day_of_week"] >= 5
    ).astype(int)

    # --------------------------------------------------------
    # Customer historical features
    # --------------------------------------------------------

    result["customer_txn_count_prior"] = (
        result.groupby("customer_id")
        .cumcount()
        .astype(float)
    )

    customer_sum = (
        result.groupby("customer_id")["amount"]
        .cumsum()
        .astype(float)
    )

    result["customer_avg_amount_prior"] = np.where(
        result["customer_txn_count_prior"] > 0,
        (
            customer_sum - result["amount"].astype(float)
        ) / result["customer_txn_count_prior"],
        0.0,
    )

    # --------------------------------------------------------
    # Merchant historical feature
    # --------------------------------------------------------

    result["merchant_txn_count_prior"] = (
        result.groupby("merchant_id")
        .cumcount()
        .astype(float)
    )

    # --------------------------------------------------------
    # Device historical feature
    # --------------------------------------------------------

    result["device_txn_count_prior"] = (
        result.groupby("device_id")
        .cumcount()
        .astype(float)
    )

    # --------------------------------------------------------
    # Clean numerical values
    # --------------------------------------------------------

    result[NUMERIC_FEATURES] = (
        result[NUMERIC_FEATURES]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
    )

    return result
