from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_transaction_api():
    response = client.post(
        "/transaction/new",
        json={
            "sender": "test_sender@example.com",
            "recipient": "test_recipient@example.com",
            "amount": 100.0,
            "signature": "test_signature"
        }
    )

    assert response.status_code == 200
    assert "message" in response.json()
