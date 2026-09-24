from pathlib import Path

import pandas as pd

from sentinelx.database.connection import SessionLocal
from sentinelx.risk.persistence_adapter import RiskPersistenceAdapter
from sentinelx.decision.engine import DecisionEngine
from sentinelx.alerts.alert_engine import AlertEngine


ROOT = Path(__file__).resolve().parents[2]

RISK_CONTEXT = (
    ROOT
    / "reports"
    / "risk"
    / "fusion"
    / "risk_context.parquet"
)


def main():

    df = pd.read_parquet(RISK_CONTEXT)

    required = {
        "transaction_id",
        "risk_score",
        "model_version",
        "risk_level",
    }

    missing = required - set(df.columns)

    if missing:
        raise RuntimeError(
            f"Missing columns: {sorted(missing)}"
        )

    # Select the highest-risk REAL transaction.
    row = df.sort_values(
        "risk_score",
        ascending=False,
    ).iloc[0]

    transaction_id = str(row["transaction_id"])
    risk_score = float(row["risk_score"])
    risk_level = str(row["risk_level"])
    model_version = str(row["model_version"])

    decision_engine = DecisionEngine()
    alert_engine = AlertEngine()

    decision_data = decision_engine.evaluate(
        transaction_id=transaction_id,
        risk_score=risk_score,
    )

    decision = decision_data["decision"]
    severity = decision_data["severity"]

    alert_data = alert_engine.create_alert(
        transaction_id=transaction_id,
        risk_score=risk_score,
        decision=decision,
        severity=severity,
        explanation=(
            f"Real risk-fusion transaction; "
            f"risk_score={risk_score:.4f}; "
            f"risk_level={risk_level}"
        ),
    )

    print("")
    print("REAL HIGH-RISK TRANSACTION")
    print("--------------------------")
    print("transaction_id:", transaction_id)
    print("risk_score:", risk_score)
    print("risk_level:", risk_level)
    print("decision:", decision)
    print("severity:", severity)
    print("alert_created:", alert_data["alert_created"])

    assert decision in {"REVIEW", "BLOCK"}
    assert alert_data["alert_created"] is True

    db = SessionLocal()

    try:
        adapter = RiskPersistenceAdapter(db)

        decision_payload = {
            "transaction_id": transaction_id,
            "risk_score": risk_score,
            "decision": decision,
            "model_version": model_version,
            "feature_version": "risk-fusion-v1",
            "rule_version": decision_data["rule_version"],
        }

        alert_payload = {
            "transaction_id": transaction_id,
            "severity": severity,
            "alert_type": "RISK",
            "message": alert_data["explanation"],
            "status": alert_data["status"],
        }

        result = adapter.persist(
            decision=decision_payload,
            alert=alert_payload,
        )

        assert result["decision"] is not None
        assert result["alert"] is not None

        assert (
            result["decision"].transaction_id
            == transaction_id
        )

        assert (
            result["alert"].transaction_id
            == transaction_id
        )

        print("")
        print("[PASS] Real high-risk decision persisted")
        print("[PASS] Real high-risk alert persisted")
        print("[PASS] Alert linked to real transaction")
        print("[PASS] PostgreSQL persistence verified")

        print("")
        print("============================================================")
        print(" PHASE 10.5 BLOCK 4 PASSED")
        print("============================================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()
