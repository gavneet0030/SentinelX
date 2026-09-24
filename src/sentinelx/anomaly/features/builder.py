"""Point-in-time-safe anomaly feature construction."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class AnomalyFeatureResult:
    frame: pd.DataFrame
    feature_columns: list[str]


def build_anomaly_features(df: pd.DataFrame) -> AnomalyFeatureResult:
    """
    Build transaction-level anomaly features.

    Important:
    - Features are derived from the current transaction and historical
      information available before the current event.
    - No future transaction information is used.
    - Rolling customer statistics are shifted before being joined to
      the current event.
    """

    required = [
        "transaction_id",
        "customer_id",
        "merchant_id",
        "timestamp",
        "amount",
        "payment_method",
        "channel",
        "country",
        "device_id",
    ]

    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    work = df.copy()

    work["timestamp"] = pd.to_datetime(
        work["timestamp"],
        utc=True,
        errors="coerce",
    )

    work["amount"] = pd.to_numeric(
        work["amount"],
        errors="coerce",
    )

    if work["timestamp"].isna().any():
        raise ValueError("Invalid timestamps detected.")

    if work["amount"].isna().any():
        raise ValueError("Invalid amounts detected.")

    work = work.sort_values(
        ["customer_id", "timestamp", "transaction_id"]
    ).reset_index(drop=True)

    # --------------------------------------------------------
    # Current-event transaction features
    # --------------------------------------------------------

    work["amount_log1p"] = np.log1p(
        work["amount"].clip(lower=0)
    )

    work["amount_is_large"] = (
        work["amount"] > work["amount"].quantile(0.95)
    ).astype(int)

    work["hour"] = work["timestamp"].dt.hour
    work["day_of_week"] = work["timestamp"].dt.dayofweek
    work["is_weekend"] = (
        work["day_of_week"] >= 5
    ).astype(int)

    work["is_night"] = (
        (work["hour"] < 6) |
        (work["hour"] >= 23)
    ).astype(int)

    # --------------------------------------------------------
    # Point-in-time customer history
    # --------------------------------------------------------

    grouped = work.groupby("customer_id", sort=False)

    work["customer_previous_count"] = (
        grouped.cumcount()
    )

    work["customer_previous_amount_sum"] = (
        grouped["amount"]
        .cumsum()
        .sub(work["amount"])
    )

    work["customer_previous_amount_mean"] = np.where(
        work["customer_previous_count"] > 0,
        work["customer_previous_amount_sum"]
        / work["customer_previous_count"],
        0.0,
    )

    # Previous amount using group shift.
    work["customer_previous_amount"] = (
        grouped["amount"].shift(1)
    )

    work["amount_vs_previous"] = (
        work["amount"]
        / work["customer_previous_amount"].replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(1.0)

    work["amount_vs_customer_mean"] = (
        work["amount"]
        / work["customer_previous_amount_mean"]
        .replace(0, np.nan)
    ).replace([np.inf, -np.inf], np.nan).fillna(1.0)

    # --------------------------------------------------------
    # Point-in-time velocity
    # --------------------------------------------------------

    work = work.sort_values(
        ["customer_id", "timestamp", "transaction_id"]
    ).reset_index(drop=True)

    work["customer_prev_timestamp"] = (
        work.groupby("customer_id")["timestamp"].shift(1)
    )

    work["seconds_since_previous"] = (
        work["timestamp"] -
        work["customer_prev_timestamp"]
    ).dt.total_seconds()

    work["seconds_since_previous"] = (
        work["seconds_since_previous"]
        .fillna(86400.0)
        .clip(lower=0)
    )

    work["customer_velocity_1h"] = 0.0
    work["customer_velocity_24h"] = 0.0

    # Explicit per-customer historical windows.
    # This is intentionally implemented without future leakage.
    for customer_id, group in work.groupby(
        "customer_id",
        sort=False,
    ):
        timestamps = group["timestamp"].tolist()

        values_1h = []
        values_24h = []

        left_1h = 0
        left_24h = 0

        for i, current_time in enumerate(timestamps):
            cutoff_1h = current_time - pd.Timedelta(hours=1)
            cutoff_24h = current_time - pd.Timedelta(hours=24)

            while (
                left_1h < i
                and timestamps[left_1h] < cutoff_1h
            ):
                left_1h += 1

            while (
                left_24h < i
                and timestamps[left_24h] < cutoff_24h
            ):
                left_24h += 1

            values_1h.append(i - left_1h)
            values_24h.append(i - left_24h)

        work.loc[group.index, "customer_velocity_1h"] = values_1h
        work.loc[group.index, "customer_velocity_24h"] = values_24h

    # --------------------------------------------------------
    # Device history
    # --------------------------------------------------------

    work["device_previous_count"] = (
        work.groupby("device_id").cumcount()
    )

    work["device_new_for_customer"] = (
        (
            work.groupby(
                ["customer_id", "device_id"]
            ).cumcount() == 0
        )
    ).astype(int)

    # --------------------------------------------------------
    # Merchant history
    # --------------------------------------------------------

    work["merchant_previous_count"] = (
        work.groupby("merchant_id").cumcount()
    )

    # --------------------------------------------------------
    # Categorical anomaly encodings
    # --------------------------------------------------------

    work["payment_method_code"] = (
        pd.factorize(work["payment_method"])[0]
    )

    work["channel_code"] = (
        pd.factorize(work["channel"])[0]
    )

    work["country_code"] = (
        pd.factorize(work["country"])[0]
    )

    # --------------------------------------------------------
    # Robust statistical features
    # --------------------------------------------------------

    work["customer_amount_deviation"] = (
        work["amount"]
        - work["customer_previous_amount_mean"]
    )

    work["customer_amount_deviation_abs"] = (
        work["customer_amount_deviation"].abs()
    )

    work["customer_history_exists"] = (
        work["customer_previous_count"] > 0
    ).astype(int)

    # --------------------------------------------------------
    # Final numeric feature set
    # --------------------------------------------------------

    feature_columns = [
        "amount",
        "amount_log1p",
        "amount_is_large",
        "hour",
        "day_of_week",
        "is_weekend",
        "is_night",
        "customer_previous_count",
        "customer_previous_amount_sum",
        "customer_previous_amount_mean",
        "customer_previous_amount",
        "amount_vs_previous",
        "amount_vs_customer_mean",
        "seconds_since_previous",
        "customer_velocity_1h",
        "customer_velocity_24h",
        "device_previous_count",
        "device_new_for_customer",
        "merchant_previous_count",
        "payment_method_code",
        "channel_code",
        "country_code",
        "customer_amount_deviation",
        "customer_amount_deviation_abs",
        "customer_history_exists",
    ]

    work[feature_columns] = (
        work[feature_columns]
        .replace([np.inf, -np.inf], np.nan)
        .fillna(0.0)
    )

    return AnomalyFeatureResult(
        frame=work,
        feature_columns=feature_columns,
    )
