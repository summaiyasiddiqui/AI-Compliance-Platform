import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


from uuid import uuid4

import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def auth_token(client):
    unique = uuid4().hex[:8]

    username = f"test_user_{unique}"
    password = "password123"

    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{unique}@example.com",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    return login_response.json()["access_token"]

