from fastapi.testclient import TestClient

from api.main import app


client = TestClient(app)


def main():
    transaction_id = "phase104_block4_001"

    risk_response = client.get(
        f"/risk/{transaction_id}"
    )

    assert risk_response.status_code == 200

    risk = risk_response.json()

    assert risk["transaction_id"] == transaction_id
    assert risk["decision"] == "REVIEW"
    assert float(risk["risk_score"]) == 72.5

    print("[PASS] GET /risk/{transaction_id}")

    alerts_response = client.get(
        "/alerts",
        params={"limit": 100},
    )

    assert alerts_response.status_code == 200

    payload = alerts_response.json()

    assert "alerts" in payload
    assert payload["count"] >= 1

    matching = [
        alert
        for alert in payload["alerts"]
        if alert["transaction_id"] == transaction_id
    ]

    assert len(matching) >= 1
    assert matching[0]["severity"] == "HIGH"
    assert matching[0]["status"] == "OPEN"

    print("[PASS] GET /alerts")
    print("[PASS] PostgreSQL risk retrieval")
    print("[PASS] PostgreSQL alert retrieval")

    print("")
    print("============================================================")
    print(" PHASE 10.4 BLOCK 5 PASSED")
    print("============================================================")


if __name__ == "__main__":
    main()
