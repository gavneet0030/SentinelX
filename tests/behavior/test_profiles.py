import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sentinelx.behavior.customer_profile import (
    build_customer_profiles,
)

from sentinelx.behavior.device_intelligence import (
    build_device_profiles,
)

from sentinelx.behavior.merchant_intelligence import (
    build_merchant_profiles,
)


def make_data():

    return pd.DataFrame(
        {
            "transaction_id": [
                "t1",
                "t2",
                "t3",
                "t4",
            ],
            "customer_id": [
                "c1",
                "c1",
                "c2",
                "c2",
            ],
            "merchant_id": [
                "m1",
                "m1",
                "m2",
                "m2",
            ],
            "device_id": [
                "d1",
                "d1",
                "d2",
                "d3",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T01:00:00Z",
                    "2026-01-01T02:00:00Z",
                    "2026-01-01T03:00:00Z",
                ]
            ),
            "amount": [
                10.0,
                20.0,
                30.0,
                40.0,
            ],
            "country": [
                "IN",
                "IN",
                "US",
                "US",
            ],
            "payment_method": [
                "card",
                "card",
                "wallet",
                "wallet",
            ],
            "is_fraud": [
                0,
                1,
                0,
                0,
            ],
        }
    )


def test_customer_profiles():

    result = build_customer_profiles(
        make_data()
    )

    assert len(result) == 2

    assert (
        result[
            "transaction_count"
        ].sum()
        == 4
    )


def test_device_profiles():

    result = build_device_profiles(
        make_data()
    )

    assert len(result) == 3

    d1 = result[
        result["device_id"] == "d1"
    ].iloc[0]

    assert d1["transaction_count"] == 2


def test_merchant_profiles():

    result = build_merchant_profiles(
        make_data()
    )

    assert len(result) == 2

    assert (
        "merchant_risk_score"
        in result.columns
    )
