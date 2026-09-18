from fastapi import APIRouter

router = APIRouter(
    prefix="/risk",
    tags=["risk"],
)


@router.get("/{event_id}")
def get_risk(event_id: str):

    return {
        "event_id": event_id,
        "status": "not_scored",
    }
