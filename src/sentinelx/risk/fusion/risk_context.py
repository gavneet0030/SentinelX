"""
Final multi-signal risk context.
"""

import pandas as pd


def prepare_risk_context(df):

    data = df.copy()

    for column in [
        "fraud_probability",
        "behavioral_risk",
        "anomaly_score"
    ]:

        data[column] = (
            pd.to_numeric(
                data[column],
                errors="coerce"
            )
            .fillna(0)
            .clip(0, 100)
        )

    behavioral_normalized = (
        data["behavioral_risk"] / 100
    )

    data["signal_strength"] = (

        data["fraud_probability"] * 0.40

        +

        behavioral_normalized * 0.30

        +

        data["anomaly_score"] * 0.30

    )

    data["signal_strength"] = (
        data["signal_strength"]
        .clip(0, 1)
    )

    data["risk_score"] = (
        data["signal_strength"] * 100
    ).round(2)

    data["risk_level"] = pd.cut(
        data["risk_score"],
        bins=[
            -1,
            30,
            60,
            85,
            100
        ],
        labels=[
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL"
        ]
    )

    return data
