from __future__ import annotations

import argparse
import random
import uuid
from datetime import datetime, timedelta, timezone
from pathlib import Path

import pandas as pd


COUNTRIES = [
    "IN",
    "US",
    "GB",
    "DE",
    "SG",
    "AE",
]

PAYMENT_METHODS = [
    "card",
    "bank_transfer",
    "wallet",
    "upi",
]

CHANNELS = [
    "web",
    "mobile",
    "pos",
]

MERCHANTS = [
    f"merchant_{i:03d}"
    for i in range(1, 21)
]

DEVICES = [
    f"device_{i:03d}"
    for i in range(1, 101)
]


def generate_transaction(
    index: int,
    rng: random.Random,
    start_time: datetime,
) -> dict:

    customer_id = (
        f"customer_{rng.randint(1, 2000):05d}"
    )

    merchant_id = rng.choice(MERCHANTS)

    timestamp = (
        start_time
        + timedelta(
            seconds=rng.randint(
                0,
                30 * 24 * 60 * 60,
            )
        )
    )

    amount = round(
        max(
            1.0,
            rng.lognormvariate(
                3.5,
                1.0,
            ),
        ),
        2,
    )

    country = rng.choice(COUNTRIES)

    fraud_probability = 0.025

    if amount > 500:
        fraud_probability += 0.10

    if country in {"US", "GB"}:
        fraud_probability += 0.02

    is_fraud = (
        rng.random()
        < fraud_probability
    )

    if is_fraud:
        amount = round(
            amount
            * rng.uniform(1.5, 5.0),
            2,
        )

    return {
        "transaction_id": (
            f"txn_{index:08d}_"
            f"{uuid.uuid4().hex[:8]}"
        ),
        "customer_id": customer_id,
        "merchant_id": merchant_id,
        "timestamp": timestamp,
        "amount": amount,
        "currency": "USD",
        "payment_method": rng.choice(
            PAYMENT_METHODS
        ),
        "channel": rng.choice(
            CHANNELS
        ),
        "country": country,
        "device_id": rng.choice(
            DEVICES
        ),
        "ip_address": (
            f"192.168."
            f"{rng.randint(0, 255)}."
            f"{rng.randint(1, 254)}"
        ),
        "is_fraud": bool(is_fraud),
    }


def generate_dataset(
    rows: int,
    seed: int = 42,
) -> pd.DataFrame:

    if rows <= 0:
        raise ValueError(
            "rows must be greater than zero"
        )

    rng = random.Random(seed)

    start_time = datetime(
        2026,
        1,
        1,
        tzinfo=timezone.utc,
    )

    records = [
        generate_transaction(
            index=i + 1,
            rng=rng,
            start_time=start_time,
        )
        for i in range(rows)
    ]

    return pd.DataFrame(records)


def main() -> None:

    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--rows",
        type=int,
        default=10000,
    )

    parser.add_argument(
        "--seed",
        type=int,
        default=42,
    )

    parser.add_argument(
        "--output",
        default="data/raw/transactions.csv",
    )

    args = parser.parse_args()

    output = Path(args.output)

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    df = generate_dataset(
        rows=args.rows,
        seed=args.seed,
    )

    df.to_csv(
        output,
        index=False,
    )

    print(
        f"[PASS] Generated {len(df):,} transactions."
    )

    print(
        f"[PASS] Output: {output}"
    )


if __name__ == "__main__":
    main()
