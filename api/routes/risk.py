from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from sentinelx.database.connection import get_db
from api.services.risk_query import RiskQueryService

router = APIRouter()


@router.get("/risk/{transaction_id}")
def get_risk(transaction_id: str, db: Session = Depends(get_db)):
    service = RiskQueryService(db)
    record = service.get_risk_decision(transaction_id)

    if record is None:
        raise HTTPException(
            status_code=404,
            detail="Risk decision not found",
        )

    return {
        "id": record.id,
        "transaction_id": record.transaction_id,
        "risk_score": float(record.risk_score),
        "decision": record.decision,
        "model_version": record.model_version,
        "feature_version": record.feature_version,
        "rule_version": record.rule_version,
        "created_at": record.created_at,
    }
