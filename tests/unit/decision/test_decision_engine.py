from src.decision.engine import make_decision
from api.schemas.risk import RiskDecision


def test_low_risk_is_approved():

    decision = make_decision(0.10)

    assert decision == RiskDecision.APPROVE


def test_medium_risk_requires_review():

    decision = make_decision(0.50)

    assert decision == RiskDecision.REVIEW


def test_high_risk_is_blocked():

    decision = make_decision(0.90)

    assert decision == RiskDecision.BLOCK
