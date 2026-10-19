import pandas as pd

from sentinelx.graph.network.builder import build_graph_edges
from sentinelx.graph.features.graph_features import build_graph_features


def sample_data():

    return pd.DataFrame(
        {
            "transaction_id": ["t1", "t2", "t3"],
            "timestamp": [
                "2026-10-01T10:00:00Z",
                "2026-10-01T10:01:00Z",
                "2026-10-01T10:02:00Z",
            ],
            "customer_id": ["c1", "c1", "c2"],
            "merchant_id": ["m1", "m2", "m1"],
            "device_id": ["d1", "d1", "d2"],
        }
    )


def test_graph_edges_build():

    result = build_graph_edges(sample_data())

    assert not result.empty
    assert len(result) == 6

    assert "transaction_id" in result.columns
    assert "source_type" in result.columns
    assert "target_type" in result.columns
    assert "source_id" in result.columns
    assert "target_id" in result.columns


def test_graph_features_build():

    result = build_graph_features(sample_data())

    assert not result.empty

    assert "transaction_id" in result.columns
    assert "customer_id" in result.columns
    assert "graph_risk_score" in result.columns
    assert "shared_device" in result.columns
    assert "shared_merchant" in result.columns

    assert result["graph_risk_score"].between(0, 100).all()

def test_same_timestamp_transactions_do_not_influence_each_other():
    frame = pd.DataFrame(
        {
            "transaction_id": ["t1", "t2", "t3"],
            "timestamp": [
                "2026-10-01T10:00:00Z",
                "2026-10-01T10:00:00Z",
                "2026-10-01T10:01:00Z",
            ],
            "customer_id": ["c1", "c2", "c3"],
            "merchant_id": ["m1", "m1", "m2"],
            "device_id": ["d1", "d1", "d1"],
        }
    )

    result = build_graph_features(frame).set_index("transaction_id")

    # Both simultaneous transactions must see the graph as it existed
    # before either transaction occurred.
    assert result.loc["t1", "device_customer_degree"] == 0
    assert result.loc["t2", "device_customer_degree"] == 0
    assert result.loc["t1", "shared_device"] == 0
    assert result.loc["t2", "shared_device"] == 0

    # The later transaction can see both earlier customers.
    assert result.loc["t3", "device_customer_degree"] == 2
    assert result.loc["t3", "shared_device"] == 1


def test_graph_features_are_independent_of_input_order_for_timestamp_ties():
    frame = pd.DataFrame(
        {
            "transaction_id": ["t2", "t1", "t3"],
            "timestamp": [
                "2026-10-01T10:00:00Z",
                "2026-10-01T10:00:00Z",
                "2026-10-01T10:01:00Z",
            ],
            "customer_id": ["c2", "c1", "c3"],
            "merchant_id": ["m1", "m1", "m2"],
            "device_id": ["d1", "d1", "d1"],
        }
    )

    first = build_graph_features(frame).sort_values("transaction_id").reset_index(drop=True)
    second = (
        build_graph_features(frame.sample(frac=1, random_state=42))
        .sort_values("transaction_id")
        .reset_index(drop=True)
    )

    pd.testing.assert_frame_equal(first, second)


def test_future_transactions_do_not_change_earlier_graph_features():
    historical = pd.DataFrame(
        {
            "transaction_id": ["t1", "t2"],
            "timestamp": [
                "2026-10-01T10:00:00Z",
                "2026-10-01T10:01:00Z",
            ],
            "customer_id": ["c1", "c2"],
            "merchant_id": ["m1", "m2"],
            "device_id": ["d1", "d1"],
        }
    )

    future = pd.DataFrame(
        {
            "transaction_id": ["t3", "t4"],
            "timestamp": [
                "2026-10-02T10:00:00Z",
                "2026-10-02T10:01:00Z",
            ],
            "customer_id": ["c3", "c1"],
            "merchant_id": ["m3", "m4"],
            "device_id": ["d1", "d9"],
        }
    )

    historical_features = (
        build_graph_features(historical)
        .set_index("transaction_id")
        .sort_index()
    )

    combined_features = (
        build_graph_features(pd.concat([historical, future], ignore_index=True))
        .set_index("transaction_id")
        .sort_index()
        .loc[historical_features.index]
    )

    pd.testing.assert_frame_equal(
        historical_features,
        combined_features,
    )
