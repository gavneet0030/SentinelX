from __future__ import annotations

import hashlib
import uuid


class AlertEngine:

    def create_alert(
        self,
        transaction_id: str,
        risk_score: float,
        decision: str,
        severity: str,
        explanation: str = "",
    ) -> dict:

        if decision == "APPROVE":
            return {
                "transaction_id": transaction_id,
                "alert_id": None,
                "case_id": None,
                "alert_created": False,
                "severity": severity,
                "decision": decision,
                "risk_score": round(float(risk_score), 4),
                "explanation": explanation,
            }

        seed = f"{transaction_id}:{risk_score}:{decision}"

        alert_id = (
            "ALT-"
            + hashlib.sha256(seed.encode()).hexdigest()[:16].upper()
        )

        case_id = (
            "CASE-"
            + uuid.uuid5(
                uuid.NAMESPACE_DNS,
                seed,
            ).hex[:16].upper()
        )

        return {
            "transaction_id": transaction_id,
            "alert_id": alert_id,
            "case_id": case_id,
            "alert_created": True,
            "severity": severity,
            "decision": decision,
            "risk_score": round(float(risk_score), 4),
            "status": "OPEN",
            "explanation": explanation,
        }
