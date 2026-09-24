from sentinelx.database.connection import SessionLocal
from sentinelx.risk.persistence_adapter import RiskPersistenceAdapter


def main():
    transaction_id = "phase105_risk_e2e_001"

    decision = {
        "transaction_id": transaction_id,
        "risk_score": 81.25,
        "decision": "REVIEW",
        "model_version": "sentinelx-model-v1",
        "feature_version": "sentinelx-features-v1",
        "rule_version": "sentinelx-rules-v1",
    }

    alert = {
        "transaction_id": transaction_id,
        "severity": "HIGH",
        "alert_type": "RISK",
        "message": "Risk engine generated a high-risk review alert.",
        "status": "OPEN",
    }

    db = SessionLocal()

    try:
        adapter = RiskPersistenceAdapter(db)

        result = adapter.persist(
            decision=decision,
            alert=alert,
        )

        decision_record = result["decision"]
        alert_record = result["alert"]

        assert decision_record is not None
        assert alert_record is not None

        assert decision_record.transaction_id == transaction_id
        assert float(decision_record.risk_score) == 81.25
        assert decision_record.decision == "REVIEW"

        assert alert_record.transaction_id == transaction_id
        assert alert_record.severity == "HIGH"
        assert alert_record.alert_type == "RISK"
        assert alert_record.status == "OPEN"

        print("[PASS] Risk engine decision persisted")
        print("[PASS] Risk engine alert persisted")
        print("[PASS] Decision linked to transaction")
        print("[PASS] Alert linked to transaction")

        print("")
        print("============================================================")
        print(" PHASE 10.5 BLOCK 2 PASSED")
        print("============================================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()
