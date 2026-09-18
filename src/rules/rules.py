"""
Deterministic risk rules.
"""


def velocity_rule(
    transactions_last_5min: int,
    threshold: int = 10,
) -> float:

    if transactions_last_5min > threshold:
        return 1.0

    return 0.0


def amount_deviation_rule(
    deviation: float,
    threshold: float,
) -> float:

    if abs(deviation) > threshold:
        return 1.0

    return 0.0
