import pytest
from fastapi.testclient import TestClient
from .app import app

client = TestClient(app)


def test_health_check_returns_json():
    """Test /health endpoint returns valid JSON response"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    
    assert data["status"] == "healthy"
    assert "timestamp" in data
    assert "model_loaded" in data
    assert "scaler_loaded" in data
