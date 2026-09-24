from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Float,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from sentinelx.database.connection import Base


class RiskDecisionRecord(Base):
    __tablename__ = "risk_decisions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    risk_score: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    decision: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    model_version: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    feature_version: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    rule_version: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AlertRecord(Base):
    __tablename__ = "alerts"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    transaction_id: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    severity: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        index=True,
    )

    alert_type: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        default="OPEN",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


class AuditEventRecord(Base):
    __tablename__ = "audit_events"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    event_type: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    transaction_id: Mapped[str | None] = mapped_column(
        String(128),
        nullable=True,
        index=True,
    )

    actor: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    details: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
