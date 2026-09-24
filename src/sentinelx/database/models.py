from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Integer,
    Numeric,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column

from sentinelx.database.connection import Base


class TransactionRecord(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
        index=True,
    )

    customer_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    merchant_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        index=True,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(18, 2),
        nullable=False,
    )

    currency: Mapped[str] = mapped_column(
        String(3),
        nullable=False,
    )

    payment_method: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    channel: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
    )

    country: Mapped[str] = mapped_column(
        String(8),
        nullable=False,
    )

    device_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    ip_address: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
