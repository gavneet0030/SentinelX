from datetime import datetime, timezone

from api.schemas.transaction import TransactionRequest
from sentinelx.database.transaction_repository import (
    TransactionRepository,
)


def main():

    transaction_id = "repository_test_001"

    transaction = TransactionRequest(
        transaction_id=transaction_id,
        customer_id="customer_repo_001",
        merchant_id="merchant_repo_001",
        timestamp=datetime.now(timezone.utc),
        amount=125.50,
        currency="USD",
        payment_method="card",
        channel="web",
        country="US",
        device_id="device_repo_001",
        ip_address="8.8.8.8",
    )

    repository = TransactionRepository()

    saved = repository.save(transaction)

    assert saved.transaction_id == transaction_id

    stored = repository.get(transaction_id)

    assert stored is not None
    assert stored.transaction_id == transaction_id
    assert float(stored.amount) == 125.50

    print("")
    print("[PASS] PostgreSQL transaction save")
    print("[PASS] PostgreSQL transaction read")
    print("[PASS] Transaction persistence verified")


if __name__ == "__main__":
    main()
