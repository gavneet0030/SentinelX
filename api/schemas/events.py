from datetime import datetime
from pydantic import BaseModel, Field


class TransactionEvent(BaseModel):
    event_id: str
    customer_id: str | None = None
    merchant_id: str | None = None
    device_id: str | None = None

    amount: float = Field(ge=0)

    timestamp: datetime

    location: str | None = None

    event_type: str = "transaction"
    source: str = "unknown"
    partition_key: str | None = None
    trace_id: str | None = None
    schema_version: str = "1.0"
