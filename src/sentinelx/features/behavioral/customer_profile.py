from __future__ import annotations

import pandas as pd


def build_customer_profiles(
    transactions: pd.DataFrame,
) -> pd.DataFrame:

    required = {
        "customer_id",
        "amount",
        "timestamp",
        "country",
        "device_id",
        "payment_method",
    }

    missing = required.difference(transactions.columns)

    if missing:
        raise ValueError(
            f"Missing customer profile columns: {sorted(missing)}"
        )

    df = transactions.copy()

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        utc=True,
    )

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    grouped = (
        df.groupby("customer_id")
        .agg(
            transaction_count=(
                "transaction_id",
                "count",
            ),
            total_amount=(
                "amount",
                "sum",
            ),
            average_amount=(
                "amount",
                "mean",
            ),
            maximum_amount=(
                "amount",
                "max",
            ),
            unique_countries=(
                "country",
                "nunique",
            ),
            unique_devices=(
                "device_id",
                "nunique",
            ),
            unique_payment_methods=(
                "payment_method",
                "nunique",
            ),
            first_transaction=(
                "timestamp",
                "min",
            ),
            last_transaction=(
                "timestamp",
                "max",
            ),
        )
        .reset_index()
    )

    grouped["transaction_frequency_per_day"] = (
        grouped["transaction_count"]
        /
        (
            (
                grouped["last_transaction"]
                -
                grouped["first_transaction"]
            ).dt.total_seconds()
            /
            86400
            + 1
        )
    )

    grouped["average_amount"] = (
        grouped["average_amount"]
        .round(2)
    )

    grouped["maximum_amount"] = (
        grouped["maximum_amount"]
        .round(2)
    )

    return grouped
