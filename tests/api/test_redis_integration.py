import uuid

from fastapi.testclient import TestClient

from api.main import app

client = TestClient(app)


def test_transaction_redis_integration():

    transaction_id = f"redis_api_test_{uuid.uuid4().hex}"

    payload = {
        "transaction_id": transaction_id,
        "customer_id": "customer_redis_001",
        "merchant_id": "merchant_001",
        "timestamp": "2026-01-01T12:00:00Z",
        "amount": 250.0,
        "currency": "USD",
        "payment_method": "card",
        "channel": "web",
        "country": "US",
        "device_id": "device_001",
        "ip_address": "8.8.8.8",
    }

    response = client.post(
        "/transactions",
        json=payload,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["transaction_id"] == transaction_id
    assert body["status"] == "accepted"
    assert body["velocity_1m"] == 1


def test_duplicate_transaction():

    transaction_id = f"redis_api_duplicate_{uuid.uuid4().hex}"

    payload = {
        "transaction_id": transaction_id,
        "customer_id": "customer_redis_002",
        "merchant_id": "merchant_002",
        "timestamp": "2026-01-01T12:00:00Z",
        "amount": 100.0,
        "currency": "USD",
        "payment_method": "card",
        "channel": "web",
        "country": "US",
        "device_id": "device_002",
        "ip_address": "8.8.8.8",
    }

    first = client.post(
        "/transactions",
        json=payload,
    )

    second = client.post(
        "/transactions",
        json=payload,
    )

    assert first.status_code == 200
    assert second.status_code == 200

    assert first.json()["status"] == "accepted"
    assert second.json()["status"] == "duplicate"
