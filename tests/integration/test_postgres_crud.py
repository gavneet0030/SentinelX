from datetime import datetime, timezone

from sqlalchemy import select

from sentinelx.database.connection import SessionLocal
from sentinelx.database.models import TransactionRecord
from sentinelx.database.decision_models import (
    RiskDecisionRecord,
    AlertRecord,
    AuditEventRecord,
)


TRANSACTION_ID = "postgres_integration_001"


def main():
    db = SessionLocal()

    try:
        # --------------------------------------------------------
        # CLEAN TEST DATA
        # --------------------------------------------------------

        existing_tx = db.scalar(
            select(TransactionRecord).where(
                TransactionRecord.transaction_id == TRANSACTION_ID
            )
        )

        if existing_tx:
            db.delete(existing_tx)

        for model in (
            RiskDecisionRecord,
            AlertRecord,
            AuditEventRecord,
        ):
            rows = db.scalars(
                select(model).where(
                    model.transaction_id == TRANSACTION_ID
                )
            ).all()

            for row in rows:
                db.delete(row)

        db.commit()

        # --------------------------------------------------------
        # TRANSACTION
        # --------------------------------------------------------

        transaction = TransactionRecord(
            transaction_id=TRANSACTION_ID,
            customer_id="customer_pg_001",
            merchant_id="merchant_pg_001",
            timestamp=datetime.now(timezone.utc),
            amount=750.50,
            currency="USD",
            payment_method="card",
            channel="web",
            country="US",
            device_id="device_pg_001",
            ip_address="8.8.8.8",
        )

        db.add(transaction)
        db.commit()
        db.refresh(transaction)

        assert transaction.id is not None

        # --------------------------------------------------------
        # RISK DECISION
        # --------------------------------------------------------

        decision = RiskDecisionRecord(
            transaction_id=TRANSACTION_ID,
            risk_score=72.5,
            decision="REVIEW",
            model_version="sentinelx-baseline-v1",
            feature_version="features-v1",
            rule_version="rules-v1",
        )

        db.add(decision)

        # --------------------------------------------------------
        # ALERT
        # --------------------------------------------------------

        alert = AlertRecord(
            transaction_id=TRANSACTION_ID,
            severity="HIGH",
            alert_type="HIGH_RISK_TRANSACTION",
            message="Transaction requires analyst review.",
            status="OPEN",
        )

        db.add(alert)

        # --------------------------------------------------------
        # AUDIT EVENT
        # --------------------------------------------------------

        audit = AuditEventRecord(
            event_type="RISK_DECISION_CREATED",
            transaction_id=TRANSACTION_ID,
            actor="sentinelx-risk-engine",
            details="Risk score 72.5 produced REVIEW decision.",
        )

        db.add(audit)

        db.commit()

        # --------------------------------------------------------
        # READ BACK
        # --------------------------------------------------------

        stored_tx = db.scalar(
            select(TransactionRecord).where(
                TransactionRecord.transaction_id == TRANSACTION_ID
            )
        )

        stored_decision = db.scalar(
            select(RiskDecisionRecord).where(
                RiskDecisionRecord.transaction_id == TRANSACTION_ID
            )
        )

        stored_alert = db.scalar(
            select(AlertRecord).where(
                AlertRecord.transaction_id == TRANSACTION_ID
            )
        )

        stored_audit = db.scalar(
            select(AuditEventRecord).where(
                AuditEventRecord.transaction_id == TRANSACTION_ID
            )
        )

        assert stored_tx is not None
        assert float(stored_tx.amount) == 750.50

        assert stored_decision is not None
        assert stored_decision.decision == "REVIEW"
        assert stored_decision.risk_score == 72.5

        assert stored_alert is not None
        assert stored_alert.severity == "HIGH"
        assert stored_alert.status == "OPEN"

        assert stored_audit is not None
        assert stored_audit.event_type == "RISK_DECISION_CREATED"

        print("")
        print("[PASS] Transaction INSERT + READ")
        print("[PASS] Risk decision INSERT + READ")
        print("[PASS] Alert INSERT + READ")
        print("[PASS] Audit event INSERT + READ")
        print("[PASS] PostgreSQL transaction committed successfully")

    finally:
        db.close()


if __name__ == "__main__":
    main()
