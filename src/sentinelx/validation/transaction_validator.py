from __future__ import annotations

import ipaddress

import pandas as pd


REQUIRED_COLUMNS = {
    "transaction_id",
    "customer_id",
    "merchant_id",
    "timestamp",
    "amount",
    "currency",
    "payment_method",
    "channel",
    "country",
    "device_id",
    "ip_address",
    "is_fraud",
}


def validate_columns(
    df: pd.DataFrame,
) -> None:

    missing = (
        REQUIRED_COLUMNS
        - set(df.columns)
    )

    if missing:
        raise ValueError(
            f"Missing columns: "
            f"{sorted(missing)}"
        )


def validate_transaction_ids(
    df: pd.DataFrame,
) -> None:

    if df["transaction_id"].isna().any():
        raise ValueError(
            "transaction_id contains null values."
        )

    if df["transaction_id"].duplicated().any():
        raise ValueError(
            "Duplicate transaction_id values detected."
        )


def validate_amounts(
    df: pd.DataFrame,
) -> None:

    values = pd.to_numeric(
        df["amount"],
        errors="coerce",
    )

    if values.isna().any():
        raise ValueError(
            "amount contains invalid values."
        )

    if (values <= 0).any():
        raise ValueError(
            "amount must be greater than zero."
        )


def validate_timestamps(
    df: pd.DataFrame,
) -> None:

    values = pd.to_datetime(
        df["timestamp"],
        errors="coerce",
        utc=True,
    )

    if values.isna().any():
        raise ValueError(
            "timestamp contains invalid values."
        )


def validate_currency(
    df: pd.DataFrame,
) -> None:

    values = (
        df["currency"]
        .astype(str)
        .str.strip()
    )

    if values.str.len().ne(3).any():
        raise ValueError(
            "currency must contain 3-letter codes."
        )


def validate_ip_addresses(
    df: pd.DataFrame,
) -> None:

    for value in df["ip_address"].dropna():

        try:
            ipaddress.ip_address(
                str(value)
            )
        except ValueError as exc:
            raise ValueError(
                f"Invalid IP address: {value}"
            ) from exc


def validate_transactions(
    df: pd.DataFrame,
) -> None:

    validate_columns(df)
    validate_transaction_ids(df)
    validate_amounts(df)
    validate_timestamps(df)
    validate_currency(df)
    validate_ip_addresses(df)
