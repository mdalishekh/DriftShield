# Unit Test Code for CI/CD Pipelines
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello World"
    }

def test_fail():
    response = client.get("/")

    assert response.status_code == 404
