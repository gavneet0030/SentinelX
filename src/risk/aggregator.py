"""
Risk aggregation.
"""


def aggregate_risk(
    ml_score: float,
    rule_score: float,
    anomaly_score: float,
    graph_score: float = 0.0,
) -> float:

    score = (
        0.50 * ml_score
        + 0.20 * rule_score
        + 0.20 * anomaly_score
        + 0.10 * graph_score
    )

    return max(0.0, min(1.0, score))
