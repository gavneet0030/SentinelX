from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class Transaction(BaseModel):
    """Canonical transaction representation used by SentinelX."""

    model_config = ConfigDict(extra="forbid")

    transaction_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    merchant_id: str = Field(min_length=1)

    timestamp: datetime

    amount: Decimal = Field(
        gt=0,
        max_digits=18,
        decimal_places=2,
    )

    currency: str = Field(
        min_length=3,
        max_length=3,
    )

    payment_method: str = Field(min_length=1)
    channel: str = Field(min_length=1)

    country: str = Field(
        min_length=2,
        max_length=2,
    )

    device_id: str = Field(min_length=1)
    ip_address: str = Field(min_length=7)

    is_fraud: bool | None = None
