from __future__ import annotations

import pandas as pd


def time_based_split(
    df: pd.DataFrame,
    train_ratio: float = 0.70,
    validation_ratio: float = 0.15,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Split chronologically into train, validation, and test sets.

    No random shuffling is used. This simulates deployment where
    models train on historical transactions and score future ones.
    """

    if not 0 < train_ratio < 1:
        raise ValueError("train_ratio must be between 0 and 1.")

    if not 0 < validation_ratio < 1:
        raise ValueError(
            "validation_ratio must be between 0 and 1."
        )

    if train_ratio + validation_ratio >= 1:
        raise ValueError(
            "train_ratio + validation_ratio must be less than 1."
        )

    if "timestamp" not in df.columns:
        raise ValueError("timestamp column is required.")

    ordered = (
        df.sort_values(
            ["timestamp", "transaction_id"]
        )
        .reset_index(drop=True)
    )

    total = len(ordered)

    train_end = int(total * train_ratio)

    validation_end = int(
        total * (train_ratio + validation_ratio)
    )

    train = ordered.iloc[:train_end].copy()

    validation = ordered.iloc[
        train_end:validation_end
    ].copy()

    test = ordered.iloc[
        validation_end:
    ].copy()

    return train, validation, test
