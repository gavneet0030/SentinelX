from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_behavioral_risk(
    transactions: pd.DataFrame,
    customer_profiles: pd.DataFrame,
    device_profiles: pd.DataFrame,
    merchant_profiles: pd.DataFrame,
    velocity_features: pd.DataFrame,
) -> pd.DataFrame:

    base = transactions.copy()

    base["amount"] = pd.to_numeric(
        base["amount"],
        errors="coerce",
    )

    result = base[
        [
            "transaction_id",
            "customer_id",
            "merchant_id",
            "device_id",
            "amount",
            "timestamp",
        ]
    ].copy()

    result = result.merge(
        customer_profiles[
            [
                "customer_id",
                "average_amount",
                "maximum_amount",
                "unique_countries",
                "unique_devices",
                "transaction_frequency_per_day",
            ]
        ],
        on="customer_id",
        how="left",
    )

    result = result.merge(
        device_profiles[
            [
                "device_id",
                "customer_count",
                "country_count",
                "device_shared",
                "device_activity_score",
            ]
        ],
        on="device_id",
        how="left",
    )

    result = result.merge(
        merchant_profiles[
            [
                "merchant_id",
                "fraud_rate",
                "merchant_risk_score",
            ]
        ],
        on="merchant_id",
        how="left",
    )

    result = result.merge(
        velocity_features[
            [
                "transaction_id",
                "customer_txn_count_1h",
                "customer_txn_count_24h",
                "device_txn_count_1h",
                "amount_vs_customer_24h",
                "velocity_score",
            ]
        ],
        on="transaction_id",
        how="left",
    )

    numeric_columns = [
        "average_amount",
        "maximum_amount",
        "unique_countries",
        "unique_devices",
        "transaction_frequency_per_day",
        "customer_count",
        "country_count",
        "device_shared",
        "device_activity_score",
        "fraud_rate",
        "merchant_risk_score",
        "customer_txn_count_1h",
        "customer_txn_count_24h",
        "device_txn_count_1h",
        "amount_vs_customer_24h",
        "velocity_score",
    ]

    result[numeric_columns] = (
        result[numeric_columns]
        .replace(
            [np.inf, -np.inf],
            np.nan,
        )
        .fillna(0)
    )

    amount_ratio = np.where(
        result["average_amount"] > 0,
        result["amount"]
        /
        result["average_amount"],
        1.0,
    )

    result["amount_vs_customer_average"] = (
        amount_ratio
    )

    amount_signal = (
        ((amount_ratio - 1) / 4)
        .clip(0, 1)
        * 25
    )

    velocity_signal = (
        result["velocity_score"]
        * 0.35
    ).clip(0, 35)

    device_signal = (
        result["device_shared"] * 10
        +
        result["device_activity_score"] * 10
    ).clip(0, 20)

    merchant_signal = (
        result["merchant_risk_score"]
        * 0.20
    ).clip(0, 20)

    behavioral_score = (
        amount_signal
        + velocity_signal
        + device_signal
        + merchant_signal
    ).clip(0, 100)

    result["behavioral_risk_score"] = (
        behavioral_score.round(2)
    )

    result["risk_level"] = pd.cut(
        result["behavioral_risk_score"],
        bins=[
            -0.01,
            30,
            60,
            80,
            100,
        ],
        labels=[
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
        ],
    ).astype(str)

    def build_signals(row):

        signals = []

        if row["amount_vs_customer_average"] >= 3:
            signals.append("amount_anomaly")

        if row["customer_txn_count_1h"] >= 3:
            signals.append("customer_velocity_spike")

        if row["device_txn_count_1h"] >= 3:
            signals.append("device_velocity_spike")

        if row["device_shared"] == 1:
            signals.append("shared_device")

        if row["merchant_risk_score"] >= 20:
            signals.append("merchant_risk")

        if not signals:
            signals.append("no_major_behavioral_signal")

        return "|".join(signals)

    result["risk_signals"] = result.apply(
        build_signals,
        axis=1,
    )

    return result
