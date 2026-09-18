"""
Configurable risk decision policy.
"""

from src.config.settings import settings
from api.schemas.risk import RiskDecision


def make_decision(
    risk_score: float,
) -> RiskDecision:

    if risk_score < settings.risk_approve_threshold:
        return RiskDecision.APPROVE

    if risk_score < settings.risk_review_threshold:
        return RiskDecision.REVIEW

    return RiskDecision.BLOCK
