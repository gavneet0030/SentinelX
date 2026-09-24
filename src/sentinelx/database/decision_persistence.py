from datetime import datetime, timezone
from sqlalchemy.orm import Session

from sentinelx.database.decision_models import (
    RiskDecisionRecord,
    AlertRecord,
)


class DecisionPersistenceService:

    def __init__(self, db: Session):
        self.db = db

    def save_decision(self, decision: dict) -> RiskDecisionRecord:
        record = RiskDecisionRecord(
            transaction_id=decision["transaction_id"],
            risk_score=float(decision["risk_score"]),
            decision=decision["decision"],
            model_version=decision.get("model_version", "prototype-v1"),
            feature_version=decision.get("feature_version", "prototype-v1"),
            rule_version=decision.get("rule_version", "prototype-v1"),
            created_at=datetime.now(timezone.utc),
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record

    def save_alert(self, alert: dict) -> AlertRecord:
        record = AlertRecord(
            transaction_id=alert["transaction_id"],
            severity=alert["severity"],
            alert_type=alert.get("alert_type", "RISK"),
            message=alert.get("message", ""),
            status=alert.get("status", "OPEN"),
            created_at=datetime.now(timezone.utc),
        )

        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)

        return record
