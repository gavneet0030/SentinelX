from sqlalchemy.orm import Session

from sentinelx.database.decision_persistence import DecisionPersistenceService


class RiskPersistenceAdapter:

    def __init__(self, db: Session):
        self.service = DecisionPersistenceService(db)

    def persist(
        self,
        decision: dict,
        alert: dict | None = None,
    ):
        decision_record = self.service.save_decision(decision)

        alert_record = None

        if alert is not None:
            alert_record = self.service.save_alert(alert)

        return {
            "decision": decision_record,
            "alert": alert_record,
        }
