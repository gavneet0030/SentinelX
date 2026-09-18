from fastapi import APIRouter

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


@router.post("")
def submit_transaction():

    return {
        "status": "accepted",
        "message": "Transaction ingestion endpoint initialized.",
    }
