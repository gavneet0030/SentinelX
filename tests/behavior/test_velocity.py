import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"

if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from sentinelx.behavior.velocity import (
    build_velocity_features,
)


def test_velocity_does_not_include_current_transaction():

    frame = pd.DataFrame(
        {
            "transaction_id": [
                "t1",
                "t2",
                "t3",
            ],
            "customer_id": [
                "c1",
                "c1",
                "c1",
            ],
            "device_id": [
                "d1",
                "d1",
                "d1",
            ],
            "timestamp": pd.to_datetime(
                [
                    "2026-01-01T00:00:00Z",
                    "2026-01-01T00:10:00Z",
                    "2026-01-01T02:00:00Z",
                ]
            ),
            "amount": [
                10.0,
                20.0,
                30.0,
            ],
        }
    )

    result = build_velocity_features(
        frame
    )

    assert (
        result.loc[
            result["transaction_id"] == "t1",
            "customer_txn_count_1h",
        ].iloc[0]
        == 0
    )

    assert (
        result.loc[
            result["transaction_id"] == "t2",
            "customer_txn_count_1h",
        ].iloc[0]
        == 1
    )

    assert (
        result.loc[
            result["transaction_id"] == "t3",
            "customer_txn_count_1h",
        ].iloc[0]
        == 0
    )
