from __future__ import annotations

import pandas as pd


def build_device_profiles(
    transactions: pd.DataFrame,
) -> pd.DataFrame:

    required = {
        "device_id",
        "customer_id",
        "transaction_id",
        "amount",
        "country",
    }

    missing = required.difference(transactions.columns)

    if missing:
        raise ValueError(
            f"Missing device columns: {sorted(missing)}"
        )

    df = transactions.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    profile = (
        df.groupby("device_id")
        .agg(
            transaction_count=(
                "transaction_id",
                "count",
            ),
            customer_count=(
                "customer_id",
                "nunique",
            ),
            country_count=(
                "country",
                "nunique",
            ),
            total_amount=(
                "amount",
                "sum",
            ),
            average_amount=(
                "amount",
                "mean",
            ),
        )
        .reset_index()
    )

    profile["device_shared"] = (
        profile["customer_count"] > 1
    ).astype(int)

    profile["device_activity_score"] = (
        profile["transaction_count"].clip(
            upper=100
        ) / 100.0
    )

    profile["device_activity_score"] = (
        profile["device_activity_score"]
        .clip(0, 1)
        .round(4)
    )

    return profile
