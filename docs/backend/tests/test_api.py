import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_query_endpoint():
    """Test query endpoint"""
    response = client.post(
        "/api/query",
        json={
            "query": "Find molecules for diabetes",
            "provider": "openai"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True

def test_usage_stats():
    """Test usage stats endpoint"""
    response = client.get("/api/usage")
    assert response.status_code == 200
    data = response.json()
    assert "tokens_used" in data
    assert "total_cost" in data