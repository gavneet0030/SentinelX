from datetime import datetime, timezone
from decimal import Decimal

from sqlalchemy import select

from sentinelx.database.connection import SessionLocal
from sentinelx.database.models import TransactionRecord


class TransactionRepository:

    def save(self, transaction) -> TransactionRecord:
        db = SessionLocal()

        try:
            existing = db.scalar(
                select(TransactionRecord).where(
                    TransactionRecord.transaction_id
                    == transaction.transaction_id
                )
            )

            if existing:
                return existing

            record = TransactionRecord(
                transaction_id=transaction.transaction_id,
                customer_id=transaction.customer_id,
                merchant_id=transaction.merchant_id,
                timestamp=transaction.timestamp,
                amount=Decimal(str(transaction.amount)),
                currency=transaction.currency,
                payment_method=transaction.payment_method,
                channel=transaction.channel,
                country=transaction.country,
                device_id=transaction.device_id,
                ip_address=transaction.ip_address,
            )

            db.add(record)
            db.commit()
            db.refresh(record)

            return record

        except Exception:
            db.rollback()
            raise

        finally:
            db.close()


    def get(self, transaction_id: str):
        db = SessionLocal()

        try:
            return db.scalar(
                select(TransactionRecord).where(
                    TransactionRecord.transaction_id
                    == transaction_id
                )
            )

        finally:
            db.close()
