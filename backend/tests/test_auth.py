from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_register_user():
    unique = uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@example.com",
            "password": "password123"
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["username"] == f"user_{unique}"
    assert data["email"] == f"{unique}@example.com"


def test_login_user():
    response = client.post(
        "/auth/login",
        data={
            "username": "summaiya",
            "password": "mypassword123"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    # Step 1: Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": "summaiya",
            "password": "password123"
        }
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    # Step 2: Access protected endpoint
    response = client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {token}"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == "summaiya"