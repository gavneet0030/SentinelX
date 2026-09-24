from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DecisionPolicy:

    approve_max: float = 30.0
    review_max: float = 60.0

    model_version: str = "baseline-v1"
    rule_version: str = "rules-v1"
    policy_version: str = "decision-v1"


class DecisionEngine:

    def __init__(
        self,
        policy: DecisionPolicy | None = None,
    ):

        self.policy = (
            policy
            if policy is not None
            else DecisionPolicy()
        )


    def decide(
        self,
        risk_score: float,
    ) -> str:

        score = float(risk_score)

        if score < self.policy.approve_max:
            return "APPROVE"

        if score < self.policy.review_max:
            return "REVIEW"

        return "BLOCK"


    def severity(
        self,
        risk_score: float,
    ) -> str:

        score = float(risk_score)

        if score < self.policy.approve_max:
            return "LOW"

        if score < self.policy.review_max:
            return "MEDIUM"

        if score < 85:
            return "HIGH"

        return "CRITICAL"


    def evaluate(
        self,
        transaction_id: str,
        risk_score: float,
    ) -> dict:

        return {
            "transaction_id":
                transaction_id,

            "risk_score":
                round(float(risk_score), 4),

            "decision":
                self.decide(risk_score),

            "severity":
                self.severity(risk_score),

            "model_version":
                self.policy.model_version,

            "rule_version":
                self.policy.rule_version,

            "policy_version":
                self.policy.policy_version,
        }
