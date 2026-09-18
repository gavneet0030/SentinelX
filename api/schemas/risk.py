from enum import Enum
from pydantic import BaseModel, Field


class RiskDecision(str, Enum):
    APPROVE = "APPROVE"
    REVIEW = "REVIEW"
    BLOCK = "BLOCK"


class RiskResult(BaseModel):
    event_id: str
    risk_score: float = Field(ge=0, le=1)
    decision: RiskDecision
    model_version: str
    feature_version: str
    reasons: list[str] = []
