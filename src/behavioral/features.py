"""
Behavioral feature engineering.
"""

import pandas as pd


def add_customer_behavior_features(
    dataframe: pd.DataFrame,
    customer_column: str = "customer_id",
    amount_column: str = "amount",
) -> pd.DataFrame:

    df = dataframe.copy()

    if customer_column not in df.columns:
        return df

    if amount_column not in df.columns:
        return df

    grouped = df.groupby(customer_column)[amount_column]

    df["customer_avg_amount"] = grouped.transform("mean")
    df["customer_median_amount"] = grouped.transform("median")

    df["amount_deviation"] = (
        df[amount_column]
        - df["customer_avg_amount"]
    )

    return df
