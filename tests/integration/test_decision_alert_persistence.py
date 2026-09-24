from sentinelx.database.connection import SessionLocal
from sentinelx.database.decision_persistence import DecisionPersistenceService


def main():
    db = SessionLocal()

    try:
        service = DecisionPersistenceService(db)

        transaction_id = "phase104_block4_001"

        decision = {
            "transaction_id": transaction_id,
            "risk_score": 72.5,
            "decision": "REVIEW",
            "model_version": "sentinelx-model-v1",
            "feature_version": "sentinelx-features-v1",
            "rule_version": "sentinelx-rules-v1",
        }

        alert = {
            "transaction_id": transaction_id,
            "severity": "HIGH",
            "alert_type": "RISK",
            "message": "High-risk transaction requires analyst review.",
            "status": "OPEN",
        }

        decision_record = service.save_decision(decision)

        assert decision_record.transaction_id == transaction_id
        assert float(decision_record.risk_score) == 72.5
        assert decision_record.decision == "REVIEW"

        alert_record = service.save_alert(alert)

        assert alert_record.transaction_id == transaction_id
        assert alert_record.severity == "HIGH"
        assert alert_record.alert_type == "RISK"
        assert alert_record.status == "OPEN"

        print("[PASS] Risk decision persisted")
        print("[PASS] Alert persisted")
        print("[PASS] Decision transaction_id:", decision_record.transaction_id)
        print("[PASS] Alert transaction_id:", alert_record.transaction_id)

        print("")
        print("============================================================")
        print(" PHASE 10.4 BLOCK 4 PASSED")
        print("============================================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()
