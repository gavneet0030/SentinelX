from sentinelx.alerts.alert_engine import (
    AlertEngine,
)


def test_approve_has_no_alert():

    engine = AlertEngine()

    result = engine.create_alert(
        transaction_id="tx-1",
        risk_score=20,
        decision="APPROVE",
        severity="LOW",
    )

    assert result["alert_created"] is False
    assert result["alert_id"] is None
    assert result["case_id"] is None


def test_review_creates_alert():

    engine = AlertEngine()

    result = engine.create_alert(
        transaction_id="tx-2",
        risk_score=45,
        decision="REVIEW",
        severity="MEDIUM",
        explanation="Elevated risk",
    )

    assert result["alert_created"] is True
    assert result["alert_id"].startswith("ALT-")
    assert result["case_id"].startswith("CASE-")
    assert result["status"] == "OPEN"


def test_block_creates_alert():

    engine = AlertEngine()

    result = engine.create_alert(
        transaction_id="tx-3",
        risk_score=80,
        decision="BLOCK",
        severity="HIGH",
    )

    assert result["alert_created"] is True
    assert result["decision"] == "BLOCK"
