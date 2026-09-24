import pandas as pd

from sentinelx.data.processing.clean import (
    clean_transactions,
)


def test_clean_transactions():

    df = pd.DataFrame(
        [
            {
                "transaction_id": " txn_001 ",
                "customer_id": " customer_001 ",
                "merchant_id": " merchant_001 ",
                "timestamp": "2026-01-01T10:00:00Z",
                "amount": "100.50",
                "currency": "usd",
                "payment_method": "card",
                "channel": "web",
                "country": "us",
                "device_id": "device_001",
                "ip_address": "192.168.1.10",
                "is_fraud": False,
            }
        ]
    )

    result = clean_transactions(df)

    assert len(result) == 1
    assert (
        result.loc[0, "transaction_id"]
        == "txn_001"
    )
    assert (
        result.loc[0, "currency"]
        == "USD"
    )
    assert (
        result.loc[0, "country"]
        == "US"
    )
    assert (
        result.loc[0, "amount"]
        == 100.50
    )
