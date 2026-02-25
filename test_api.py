from fastapi.testclient import TestClient
from main import app
import json

client = TestClient(app)

def test_how_many_assets():
    payload = {
        "session_id": "test_session",
        "message": "How many assets do I have?",
        "context": {}
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\nQuestion: {payload['message']}")
    print(f"SQL: {data['sql_query']}")
    print(f"Answer: {data['natural_language_answer']}")
    assert data["status"] == "ok"
    assert "SELECT COUNT(*)" in data["sql_query"]
    # Since we seeded 3 active assets (excluding Disposed)
    assert "3" in data["natural_language_answer"]

def test_how_many_assets_by_site():
    payload = {
        "session_id": "test_session",
        "message": "How many assets by site?",
        "context": {}
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\nQuestion: {payload['message']}")
    print(f"SQL: {data['sql_query']}")
    print(f"Answer: {data['natural_language_answer']}")
    assert data["status"] == "ok"
    assert "GROUP BY" in data["sql_query"]

def test_total_value_per_site():
    payload = {
        "session_id": "test_session",
        "message": "Total value of assets per site",
        "context": {}
    }
    response = client.post("/api/chat", json=payload)
    assert response.status_code == 200
    data = response.json()
    print(f"\nQuestion: {payload['message']}")
    print(f"SQL: {data['sql_query']}")
    print(f"Answer: {data['natural_language_answer']}")
    assert data["status"] == "ok"
    assert "SUM(a.Cost)" in data["sql_query"] or "SUM(Cost)" in data["sql_query"]

if __name__ == "__main__":
    test_how_many_assets()
    test_how_many_assets_by_site()
    test_total_value_per_site()
