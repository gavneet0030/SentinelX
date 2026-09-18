from src.risk.aggregator import aggregate_risk


def test_risk_score_is_bounded():

    score = aggregate_risk(
        ml_score=1.0,
        rule_score=1.0,
        anomaly_score=1.0,
        graph_score=1.0,
    )

    assert 0.0 <= score <= 1.0
