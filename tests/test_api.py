from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_risk_profile_moderate():
    payload = {
        "crypto_interest": "long_term",
        "net_worth_percent": 15,
        "holding_period": "long",
        "themes": ["ai_x_crypto", "infrastructure"],
        "reaction_to_50pct_drop": "hold",
        "max_drawdown_percent": 20,
        "expected_annual_return_percent": 18
    }
    r = client.post("/v1/risk-profile", json=payload)
    assert r.status_code == 200
    body = r.json()
    assert "risk_profile" in body
    assert "risk_score" in body
    assert "reasons" in body
