from fastapi.testclient import TestClient
from sqlalchemy import select

from api.main import app

from sentinelx.database.connection import SessionLocal
from sentinelx.database.models import TransactionRecord


client = TestClient(app)

TRANSACTION_ID = "phase104_e2e_001"


def main():

    payload = {
        "transaction_id": TRANSACTION_ID,
        "customer_id": "customer_e2e_001",
        "merchant_id": "merchant_e2e_001",
        "timestamp": "2026-09-19T12:00:00Z",
        "amount": 425.75,
        "currency": "USD",
        "payment_method": "card",
        "channel": "web",
        "country": "US",
        "device_id": "device_e2e_001",
        "ip_address": "8.8.8.8",
    }

    # --------------------------------------------------------
    # FIRST API REQUEST
    # --------------------------------------------------------

    response = client.post(
        "/transactions",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["transaction_id"] == TRANSACTION_ID
    assert body["status"] == "accepted"
    assert body["persistence"] == "postgresql"
    assert body["hot_state"] == "redis"
    assert body["velocity_1m"] >= 1

    print("")
    print("[PASS] FastAPI transaction accepted")
    print("[PASS] Redis hot state updated")
    print("[PASS] PostgreSQL persistence reported")


    # --------------------------------------------------------
    # POSTGRESQL VERIFICATION
    # --------------------------------------------------------

    db = SessionLocal()

    try:

        stored = db.scalar(
            select(TransactionRecord).where(
                TransactionRecord.transaction_id
                == TRANSACTION_ID
            )
        )

        assert stored is not None
        assert stored.customer_id == "customer_e2e_001"
        assert float(stored.amount) == 425.75

        print("[PASS] PostgreSQL transaction verified")

    finally:
        db.close()


    # --------------------------------------------------------
    # DUPLICATE API REQUEST
    # --------------------------------------------------------

    duplicate = client.post(
        "/transactions",
        json=payload,
    )

    assert duplicate.status_code == 200

    duplicate_body = duplicate.json()

    assert duplicate_body["transaction_id"] == TRANSACTION_ID
    assert duplicate_body["status"] == "duplicate"

    print("[PASS] Redis duplicate detection verified")

    print("")
    print("[PASS] FULL API -> REDIS -> POSTGRESQL FLOW")


if __name__ == "__main__":
    main()
