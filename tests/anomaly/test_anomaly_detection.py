import numpy as np
import pandas as pd

from sentinelx.anomaly.features.builder import (
    build_anomaly_features,
)
from sentinelx.anomaly.models.isolation_forest import (
    AnomalyModelConfig,
    IsolationForestAnomalyModel,
)
from sentinelx.anomaly.scoring.scorer import (
    build_anomaly_output,
    minmax_normalize,
)


def make_test_data() -> pd.DataFrame:
    timestamps = pd.date_range(
        "2026-01-01",
        periods=20,
        freq="h",
        tz="UTC",
    )

    return pd.DataFrame(
        {
            "transaction_id": [
                f"T{i:04d}"
                for i in range(20)
            ],
            "customer_id": [
                "C001" if i < 10 else "C002"
                for i in range(20)
            ],
            "merchant_id": [
                "M001"
                for _ in range(20)
            ],
            "timestamp": timestamps,
            "amount": [
                20.0,
                25.0,
                22.0,
                24.0,
                21.0,
                23.0,
                26.0,
                22.0,
                24.0,
                5000.0,
                30.0,
                31.0,
                32.0,
                29.0,
                35.0,
                30.0,
                33.0,
                31.0,
                32.0,
                6000.0,
            ],
            "currency": ["USD"] * 20,
            "payment_method": [
                "card"
                for _ in range(20)
            ],
            "channel": [
                "web"
                for _ in range(20)
            ],
            "country": [
                "US"
                for _ in range(20)
            ],
            "device_id": [
                "D001" if i < 10 else "D002"
                for i in range(20)
            ],
        }
    )


def test_feature_builder_creates_features():
    df = make_test_data()

    result = build_anomaly_features(df)

    assert len(result.frame) == 20
    assert len(result.feature_columns) > 10

    for column in result.feature_columns:
        assert column in result.frame.columns


def test_features_are_numeric_and_finite():
    df = make_test_data()

    result = build_anomaly_features(df)

    values = result.frame[
        result.feature_columns
    ].to_numpy()

    assert np.isfinite(values).all()


def test_customer_history_does_not_use_future_amount():
    df = make_test_data()

    result = build_anomaly_features(df)

    first_customer_rows = result.frame[
        result.frame["customer_id"] == "C001"
    ].sort_values("timestamp")

    # First event cannot know any previous amount.
    assert (
        first_customer_rows.iloc[0][
            "customer_previous_count"
        ] == 0
    )

    # The second event can only see the first event.
    assert (
        first_customer_rows.iloc[1][
            "customer_previous_count"
        ] == 1
    )


def test_velocity_uses_only_previous_events():
    df = make_test_data()

    result = build_anomaly_features(df)

    first_customer_rows = result.frame[
        result.frame["customer_id"] == "C001"
    ].sort_values("timestamp")

    assert (
        first_customer_rows.iloc[0][
            "customer_velocity_1h"
        ] == 0
    )

    assert (
        first_customer_rows.iloc[1][
            "customer_velocity_1h"
        ] == 1
    )


def test_isolation_forest_fit_and_score():
    df = make_test_data()

    result = build_anomaly_features(df)

    model = IsolationForestAnomalyModel(
        AnomalyModelConfig(
            contamination=0.10,
            n_estimators=50,
            random_state=42,
            n_jobs=1,
        )
    )

    model.fit(
        result.frame,
        result.feature_columns,
    )

    scores = model.score_samples(
        result.frame
    )

    assert len(scores) == len(df)
    assert np.isfinite(scores).all()


def test_anomaly_scores_are_normalized():
    values = np.array(
        [1.0, 2.0, 3.0, 4.0]
    )

    normalized = minmax_normalize(values)

    assert normalized.min() == 0.0
    assert normalized.max() == 1.0


def test_anomaly_output_contains_required_fields():
    df = make_test_data()

    result = build_anomaly_features(df)

    raw_scores = np.linspace(
        0.1,
        1.0,
        len(df),
    )

    output = build_anomaly_output(
        result.frame,
        raw_scores,
    )

    required = {
        "anomaly_raw_score",
        "anomaly_score",
        "anomaly_decision",
        "anomaly_rank_percentile",
        "anomaly_signal",
    }

    assert required.issubset(
        output.columns
    )
