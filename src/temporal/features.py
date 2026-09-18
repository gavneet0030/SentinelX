"""
Temporal and velocity feature engineering.
"""

import pandas as pd


def add_temporal_features(
    dataframe: pd.DataFrame,
    timestamp_column: str = "timestamp",
) -> pd.DataFrame:

    df = dataframe.copy()

    if timestamp_column not in df.columns:
        return df

    df[timestamp_column] = pd.to_datetime(
        df[timestamp_column],
        errors="coerce",
        utc=True,
    )

    df["transaction_hour"] = (
        df[timestamp_column].dt.hour
    )

    df["transaction_day_of_week"] = (
        df[timestamp_column].dt.dayofweek
    )

    return df
