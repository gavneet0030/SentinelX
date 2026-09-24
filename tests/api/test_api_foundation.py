from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["service"] == "SentinelX"


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_model_info():
    response = client.get("/model/info")
    assert response.status_code == 200


def test_transaction():
    payload = {
        "transaction_id": "tx_test_001",
        "customer_id": "cust_001",
        "merchant_id": "merchant_001",
        "timestamp": "2026-01-01T12:00:00Z",
        "amount": 100.0,
        "currency": "USD",
        "payment_method": "card",
        "channel": "web",
        "country": "US",
        "device_id": "device_001",
        "ip_address": "8.8.8.8"
    }

    response = client.post(
        "/transactions",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json()["status"] == "accepted"
