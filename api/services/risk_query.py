from sqlalchemy.orm import Session

from sentinelx.database.decision_models import RiskDecisionRecord, AlertRecord


class RiskQueryService:

    def __init__(self, db: Session):
        self.db = db

    def get_risk_decision(self, transaction_id: str):
        return (
            self.db.query(RiskDecisionRecord)
            .filter(RiskDecisionRecord.transaction_id == transaction_id)
            .order_by(RiskDecisionRecord.created_at.desc())
            .first()
        )

    def get_alerts(self, limit: int = 100):
        return (
            self.db.query(AlertRecord)
            .order_by(AlertRecord.created_at.desc())
            .limit(limit)
            .all()
        )
