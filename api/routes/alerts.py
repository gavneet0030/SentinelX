from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from sentinelx.database.connection import get_db
from api.services.risk_query import RiskQueryService

router = APIRouter()


@router.get("/alerts")
def get_alerts(
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    service = RiskQueryService(db)
    records = service.get_alerts(limit)

    return {
        "count": len(records),
        "alerts": [
            {
                "id": record.id,
                "transaction_id": record.transaction_id,
                "severity": record.severity,
                "alert_type": record.alert_type,
                "message": record.message,
                "status": record.status,
                "created_at": record.created_at,
            }
            for record in records
        ],
    }
