from fastapi import APIRouter

from api.schemas.transaction import TransactionRequest
from api.services.transaction_state import (
    TransactionStateService,
)


router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
)


state_service = TransactionStateService()


@router.post("")
def submit_transaction(
    transaction: TransactionRequest,
):

    return state_service.process(
        transaction
    )
