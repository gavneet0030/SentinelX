from api.schemas.transaction import TransactionRequest

from sentinelx.database.transaction_repository import (
    TransactionRepository,
)
from sentinelx.state.redis_store import RedisStateStore


class TransactionStateService:

    def __init__(self):
        self.redis = RedisStateStore()
        self.repository = TransactionRepository()

    def process(self, transaction: TransactionRequest):

        transaction_key = (
            f"sentinelx:transaction:"
            f"{transaction.transaction_id}"
        )

        # --------------------------------------------------------
        # REDIS: DUPLICATE CHECK
        # --------------------------------------------------------

        if self.redis.exists(transaction_key):

            return {
                "transaction_id": transaction.transaction_id,
                "status": "duplicate",
                "velocity_1m": None,
                "persistence": "already_exists",
            }

        # --------------------------------------------------------
        # POSTGRESQL: DURABLE TRANSACTION
        # --------------------------------------------------------

        stored = self.repository.save(transaction)

        # --------------------------------------------------------
        # REDIS: VELOCITY
        # --------------------------------------------------------

        velocity_key = (
            f"sentinelx:velocity:customer:"
            f"{transaction.customer_id}:1m"
        )

        velocity = self.redis.increment(
            velocity_key,
            ttl_seconds=60,
        )

        # --------------------------------------------------------
        # REDIS: HOT TRANSACTION STATE
        # --------------------------------------------------------

        self.redis.set_json(
            transaction_key,
            {
                "transaction_id": transaction.transaction_id,
                "customer_id": transaction.customer_id,
                "merchant_id": transaction.merchant_id,
                "amount": float(transaction.amount),
                "currency": transaction.currency,
                "timestamp": str(transaction.timestamp),
                "status": "accepted",
            },
            ttl_seconds=3600,
        )

        return {
            "transaction_id": stored.transaction_id,
            "status": "accepted",
            "velocity_1m": velocity,
            "persistence": "postgresql",
            "hot_state": "redis",
        }
