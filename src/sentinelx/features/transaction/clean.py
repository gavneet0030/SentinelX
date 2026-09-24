from __future__ import annotations

import pandas as pd


def clean_transactions(
    df: pd.DataFrame,
) -> pd.DataFrame:

    result = df.copy()

    result["timestamp"] = pd.to_datetime(
        result["timestamp"],
        errors="coerce",
        utc=True,
    )

    result["amount"] = pd.to_numeric(
        result["amount"],
        errors="coerce",
    )

    string_columns = [
        "transaction_id",
        "customer_id",
        "merchant_id",
        "payment_method",
        "channel",
        "country",
        "device_id",
        "ip_address",
    ]

    for column in string_columns:

        result[column] = (
            result[column]
            .astype(str)
            .str.strip()
        )

    result["currency"] = (
        result["currency"]
        .astype(str)
        .str.strip()
        .str.upper()
    )

    result["country"] = (
        result["country"]
        .str.upper()
    )

    result = (
        result
        .dropna(
            subset=[
                "transaction_id",
                "customer_id",
                "merchant_id",
                "timestamp",
                "amount",
            ]
        )
        .drop_duplicates(
            subset=[
                "transaction_id"
            ]
        )
        .sort_values(
            "timestamp"
        )
        .reset_index(
            drop=True
        )
    )

    return result
