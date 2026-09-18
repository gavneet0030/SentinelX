"""
Dataset validation utilities.
"""

import pandas as pd


def validate_required_columns(
    dataframe: pd.DataFrame,
    required_columns: list[str],
) -> None:
    missing = [
        column
        for column in required_columns
        if column not in dataframe.columns
    ]

    if missing:
        raise ValueError(
            f"Missing required columns: {missing}"
        )


def validate_no_duplicate_event_ids(
    dataframe: pd.DataFrame,
    event_id_column: str = "event_id",
) -> None:
    if event_id_column not in dataframe.columns:
        return

    duplicates = dataframe[event_id_column].duplicated().sum()

    if duplicates > 0:
        raise ValueError(
            f"Found {duplicates} duplicate event IDs."
        )
