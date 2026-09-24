import pandas as pd
import pytest

from sentinelx.data.validation.transaction_validator import (
    validate_transactions,
)


def valid_dataframe():

    return pd.DataFrame(
        [
            {
                "transaction_id": "txn_001",
                "customer_id": "customer_001",
                "merchant_id": "merchant_001",
                "timestamp": "2026-01-01T10:00:00Z",
                "amount": 100.50,
                "currency": "USD",
                "payment_method": "card",
                "channel": "web",
                "country": "US",
                "device_id": "device_001",
                "ip_address": "192.168.1.10",
                "is_fraud": False,
            }
        ]
    )


def test_valid_transaction():

    validate_transactions(
        valid_dataframe()
    )


def test_negative_amount():

    df = valid_dataframe()

    df.loc[0, "amount"] = -10

    with pytest.raises(ValueError):

        validate_transactions(df)


def test_duplicate_transaction_id():

    df = pd.concat(
        [
            valid_dataframe(),
            valid_dataframe(),
        ],
        ignore_index=True,
    )

    with pytest.raises(ValueError):

        validate_transactions(df)


def test_invalid_ip():

    df = valid_dataframe()

    df.loc[0, "ip_address"] = (
        "invalid-ip"
    )

    with pytest.raises(ValueError):

        validate_transactions(df)
