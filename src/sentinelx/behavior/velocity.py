from __future__ import annotations

import numpy as np
import pandas as pd


def build_velocity_features(
    transactions: pd.DataFrame,
) -> pd.DataFrame:

    required = {
        "transaction_id",
        "customer_id",
        "device_id",
        "timestamp",
        "amount",
    }

    missing = required.difference(transactions.columns)

    if missing:
        raise ValueError(
            f"Missing velocity columns: {sorted(missing)}"
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

    df = (
        df.sort_values(
            ["timestamp", "transaction_id"]
        )
        .reset_index(drop=True)
    )

    timestamps = df["timestamp"]

    customer_counts = []

    device_counts = []

    customer_amounts = []

    for index in range(len(df)):

        current_time = timestamps.iloc[index]

        start_1h = current_time - pd.Timedelta(hours=1)
        start_24h = current_time - pd.Timedelta(hours=24)

        previous = df.iloc[:index]

        customer_id = df.iloc[index]["customer_id"]
        device_id = df.iloc[index]["device_id"]

        customer_previous = previous[
            previous["customer_id"] == customer_id
        ]

        device_previous = previous[
            previous["device_id"] == device_id
        ]

        customer_1h = customer_previous[
            customer_previous["timestamp"] >= start_1h
        ]

        customer_24h = customer_previous[
            customer_previous["timestamp"] >= start_24h
        ]

        device_1h = device_previous[
            device_previous["timestamp"] >= start_1h
        ]

        customer_counts.append(
            (
                len(customer_1h),
                len(customer_24h),
                len(device_1h),
            )
        )

        if len(customer_24h):
            customer_amounts.append(
                customer_24h["amount"].mean()
            )
        else:
            customer_amounts.append(0.0)

    velocity = pd.DataFrame(
        customer_counts,
        columns=[
            "customer_txn_count_1h",
            "customer_txn_count_24h",
            "device_txn_count_1h",
        ],
    )

    velocity["customer_avg_amount_24h"] = (
        customer_amounts
    )

    velocity["current_amount"] = (
        df["amount"].values
    )

    velocity["amount_vs_customer_24h"] = np.where(
        velocity["customer_avg_amount_24h"] > 0,
        velocity["current_amount"]
        /
        velocity["customer_avg_amount_24h"],
        1.0,
    )

    velocity["velocity_score"] = (
        velocity["customer_txn_count_1h"] * 15
        +
        velocity["customer_txn_count_24h"] * 2
        +
        velocity["device_txn_count_1h"] * 10
    )

    velocity["velocity_score"] = (
        velocity["velocity_score"]
        .clip(0, 100)
    )

    result = pd.concat(
        [
            df[
                [
                    "transaction_id",
                    "customer_id",
                    "device_id",
                ]
            ].reset_index(drop=True),
            velocity.reset_index(drop=True),
        ],
        axis=1,
    )

    return result
