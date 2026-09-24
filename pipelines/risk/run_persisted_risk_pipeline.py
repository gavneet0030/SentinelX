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

    if not RISK_CONTEXT.exists():
        raise FileNotFoundError(
            f"Risk context not found: {RISK_CONTEXT}"
        )

    df = pd.read_parquet(RISK_CONTEXT)

    required = {
        "transaction_id",
        "risk_score",
        "model_version",
    }

    missing = required - set(df.columns)

    if missing:
        raise RuntimeError(
            f"Missing required risk columns: {sorted(missing)}"
        )

    decision_engine = DecisionEngine()
    alert_engine = AlertEngine()

    db = SessionLocal()

    persisted_decisions = 0
    persisted_alerts = 0

    try:
        adapter = RiskPersistenceAdapter(db)

        # Small deterministic integration sample from the REAL
        # generated risk context.
        sample = df.head(25)

        for row in sample.itertuples(index=False):

            transaction_id = str(row.transaction_id)
            risk_score = float(row.risk_score)

            decision_data = decision_engine.evaluate(
                transaction_id=transaction_id,
                risk_score=risk_score,
            )

            decision = decision_data["decision"]
            severity = decision_data["severity"]

            decision_payload = {
                "transaction_id": transaction_id,
                "risk_score": risk_score,
                "decision": decision,
                "model_version": str(row.model_version),
                "feature_version": "risk-fusion-v1",
                "rule_version": decision_data["rule_version"],
            }

            alert_data = alert_engine.create_alert(
                transaction_id=transaction_id,
                risk_score=risk_score,
                decision=decision,
                severity=severity,
                explanation=(
                    f"Risk fusion score={risk_score:.4f}; "
                    f"risk_level={getattr(row, 'risk_level', 'UNKNOWN')}"
                ),
            )

            alert_payload = None

            if alert_data["alert_created"]:
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

            persisted_decisions += 1

            if result["alert"] is not None:
                persisted_alerts += 1

        print(f"[PASS] Real risk decisions persisted: {persisted_decisions}")
        print(f"[PASS] Real alerts persisted: {persisted_alerts}")
        print("[PASS] Fusion ? Decision ? Alert ? PostgreSQL")

        print("")
        print("============================================================")
        print(" PHASE 10.5 BLOCK 3 PASSED")
        print("============================================================")

    finally:
        db.close()


if __name__ == "__main__":
    main()
