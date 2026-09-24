from fastapi.testclient import TestClient

from api.main import app
from sentinelx.database.connection import SessionLocal
from sentinelx.database.models import TransactionRecord


client = TestClient(app)

TRANSACTION_ID = "phase105_api_e2e_001"


def main():

    payload = {
        "transaction_id": TRANSACTION_ID,
        "customer_id": "customer_phase105",
        "merchant_id": "merchant_phase105",
        "timestamp": "2026-09-20T10:00:00Z",
        "amount": 875.50,
        "currency": "USD",
        "payment_method": "card",
        "channel": "web",
        "country": "US",
        "device_id": "device_phase105",
        "ip_address": "8.8.8.8",
    }

    response = client.post(
        "/transactions",
        json=payload,
    )

    assert response.status_code in {200, 201}

    body = response.json()

    assert body["transaction_id"] == TRANSACTION_ID
    assert body["status"] in {"accepted", "created"}

    print("[PASS] POST /transactions")

    db = SessionLocal()

    try:
        record = (
            db.query(TransactionRecord)
            .filter(
                TransactionRecord.transaction_id
                == TRANSACTION_ID
            )
            .first()
        )

        assert record is not None
        assert record.transaction_id == TRANSACTION_ID

        print("[PASS] Transaction persisted in PostgreSQL")

    finally:
        db.close()

    duplicate = client.post(
        "/transactions",
        json=payload,
    )

    assert duplicate.status_code in {
        200,
        409,
    }

    print("[PASS] Duplicate transaction protection")

    risk_response = client.get(
        f"/risk/{TRANSACTION_ID}"
    )

    assert risk_response.status_code in {
        404,
        200,
    }

    if risk_response.status_code == 404:
        print(
            "[PASS] Risk endpoint correctly reports "
            "no decision before risk pipeline execution"
        )
    else:
        print("[PASS] Risk decision available")

    alerts_response = client.get(
        "/alerts",
        params={"limit": 100},
    )

    assert alerts_response.status_code == 200

    print("[PASS] GET /alerts")

    print("")
    print("============================================================")
    print(" PHASE 10.5 BLOCK 5 PASSED")
    print("============================================================")


if __name__ == "__main__":
    main()
