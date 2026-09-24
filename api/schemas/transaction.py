from datetime import datetime

from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):

    transaction_id: str = Field(min_length=1)

    customer_id: str = Field(min_length=1)

    merchant_id: str = Field(min_length=1)

    timestamp: datetime

    amount: float = Field(gt=0)

    currency: str = Field(min_length=3, max_length=3)

    payment_method: str

    channel: str

    country: str

    device_id: str

    ip_address: str
