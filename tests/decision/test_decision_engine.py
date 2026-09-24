from sentinelx.decision.engine import (
    DecisionEngine,
    DecisionPolicy,
)


def test_approve():

    engine = DecisionEngine()

    result = engine.evaluate(
        "tx-1",
        20,
    )

    assert result["decision"] == "APPROVE"
    assert result["severity"] == "LOW"


def test_review():

    engine = DecisionEngine()

    result = engine.evaluate(
        "tx-2",
        45,
    )

    assert result["decision"] == "REVIEW"
    assert result["severity"] == "MEDIUM"


def test_block():

    engine = DecisionEngine()

    result = engine.evaluate(
        "tx-3",
        75,
    )

    assert result["decision"] == "BLOCK"
    assert result["severity"] == "HIGH"


def test_critical():

    engine = DecisionEngine()

    result = engine.evaluate(
        "tx-4",
        90,
    )

    assert result["decision"] == "BLOCK"
    assert result["severity"] == "CRITICAL"
