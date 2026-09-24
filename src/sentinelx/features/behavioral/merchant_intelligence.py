from __future__ import annotations

import pandas as pd


def build_merchant_profiles(
    transactions: pd.DataFrame,
) -> pd.DataFrame:

    required = {
        "merchant_id",
        "transaction_id",
        "amount",
    }

    missing = required.difference(transactions.columns)

    if missing:
        raise ValueError(
            f"Missing merchant columns: {sorted(missing)}"
        )

    df = transactions.copy()

    df["amount"] = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    aggregations = {
        "transaction_count": (
            "transaction_id",
            "count",
        ),
        "total_amount": (
            "amount",
            "sum",
        ),
        "average_amount": (
            "amount",
            "mean",
        ),
    }

    if "is_fraud" in df.columns:
        aggregations["fraud_count"] = (
            "is_fraud",
            "sum",
        )

    profile = (
        df.groupby("merchant_id")
        .agg(**aggregations)
        .reset_index()
    )

    if "fraud_count" in profile.columns:
        profile["fraud_rate"] = (
            profile["fraud_count"]
            /
            profile["transaction_count"]
        )
    else:
        profile["fraud_rate"] = 0.0

    profile["merchant_volume_score"] = (
        profile["transaction_count"]
        /
        profile["transaction_count"].max()
    ).fillna(0)

    profile["merchant_risk_score"] = (
        (
            profile["fraud_rate"] * 70
        )
        +
        (
            profile["merchant_volume_score"] * 30
        )
    ).clip(0, 100)

    profile["fraud_rate"] = (
        profile["fraud_rate"]
        .round(6)
    )

    profile["merchant_risk_score"] = (
        profile["merchant_risk_score"]
        .round(2)
    )

    return profile
