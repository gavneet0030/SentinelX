import pandas as pd

from sentinelx.graph.network.builder import build_graph_edges
from sentinelx.graph.features.graph_features import build_graph_features


def sample_data():

    return pd.DataFrame(
        {
            "transaction_id": ["t1", "t2", "t3"],
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
