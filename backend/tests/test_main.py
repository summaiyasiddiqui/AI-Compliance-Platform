from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home():
    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["project"] == "ComplianceAI"
    assert data["version"] == "1.0.0"
    assert data["developer"] == "Summaiya Nadeem"
    assert data["message"] == "Welcome to ComplianceAI API!"
    from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)