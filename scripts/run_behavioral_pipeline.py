from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
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

from sentinelx.behavior.velocity import (
    build_velocity_features,
)

from sentinelx.behavior.risk_engine import (
    calculate_behavioral_risk,
)


DATA_PATH = (
    ROOT
    / "data"
    / "processed"
    / "transactions.parquet"
)

OUTPUT = (
    ROOT
    / "reports"
    / "behavior"
)


def main():

    OUTPUT.mkdir(
        parents=True,
        exist_ok=True,
    )

    print("")
    print("=" * 60)
    print(" SENTINELX BEHAVIORAL INTELLIGENCE ENGINE")
    print("=" * 60)

    print("")
    print("Loading transactions...")

    transactions = pd.read_parquet(
        DATA_PATH
    )

    print(
        f"Transactions: {len(transactions):,}"
    )

    print("")
    print("[1/5] Building customer profiles...")

    customers = build_customer_profiles(
        transactions
    )

    customers.to_parquet(
        OUTPUT / "customer_profiles.parquet",
        index=False,
    )

    print(
        f"Customer profiles: {len(customers):,}"
    )

    print("")
    print("[2/5] Building device profiles...")

    devices = build_device_profiles(
        transactions
    )

    devices.to_parquet(
        OUTPUT / "device_profiles.parquet",
        index=False,
    )

    print(
        f"Device profiles: {len(devices):,}"
    )

    print("")
    print("[3/5] Building merchant profiles...")

    merchants = build_merchant_profiles(
        transactions
    )

    merchants.to_parquet(
        OUTPUT / "merchant_profiles.parquet",
        index=False,
    )

    print(
        f"Merchant profiles: {len(merchants):,}"
    )

    print("")
    print("[4/5] Building velocity features...")

    velocity = build_velocity_features(
        transactions
    )

    velocity.to_parquet(
        OUTPUT / "velocity_features.parquet",
        index=False,
    )

    print(
        f"Velocity rows: {len(velocity):,}"
    )

    print("")
    print("[5/5] Calculating behavioral risk...")

    risk = calculate_behavioral_risk(
        transactions=transactions,
        customer_profiles=customers,
        device_profiles=devices,
        merchant_profiles=merchants,
        velocity_features=velocity,
    )

    risk.to_parquet(
        OUTPUT / "behavioral_risk.parquet",
        index=False,
    )

    risk.to_csv(
        OUTPUT / "behavioral_risk.csv",
        index=False,
    )

    print("")
    print("=" * 60)
    print(" BEHAVIORAL RISK SUMMARY")
    print("=" * 60)

    print("")
    print(
        risk[
            "risk_level"
        ]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("")
    print(
        "Average behavioral risk:",
        round(
            risk["behavioral_risk_score"].mean(),
            2,
        ),
    )

    print(
        "Maximum behavioral risk:",
        round(
            risk["behavioral_risk_score"].max(),
            2,
        ),
    )

    print("")
    print("Top behavioral signals:")

    print(
        risk["risk_signals"]
        .str.split("|")
        .explode()
        .value_counts()
        .head(10)
        .to_string()
    )

    print("")
    print("=" * 60)
    print(" PHASE 3 BEHAVIORAL ENGINE COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
