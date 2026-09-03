# All Error test will be here
import pytest
from fastapi.testclient import TestClient
from .app import app

client = TestClient(app)


def test_health_check_invalid_method():
    """Test /health endpoint with POST method (should fail)"""
    response = client.post("/health")
    
    assert response.status_code == 405  # Method Not Allowed
