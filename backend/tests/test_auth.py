from datetime import datetime, timezone
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
            "password": "password123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert "id" in data
    assert data["username"] == f"user_{unique}"
    assert data["email"] == f"{unique}@example.com"


def test_login_user():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
    password = "password123"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{unique}@example.com",
            "password": password,
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_get_current_user():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
    password = "password123"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{unique}@example.com",
            "password": password,
        },
    )

    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    token = login_response.json()["access_token"]

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["username"] == username


def test_login_wrong_password():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
    password = "password123"

    client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{unique}@example.com",
            "password": password,
        },
    )

    response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "wrongpassword",
        },
    )

    assert response.status_code == 401


def test_login_nonexistent_user():
    unique = uuid4().hex[:8]

    response = client.post(
        "/auth/login",
        data={
            "username": f"nonexistent_{unique}",
            "password": "password123",
        },
    )

    assert response.status_code == 401


def test_register_duplicate_username():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
    email = f"{unique}@example.com"

    first_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"another_{unique}@example.com",
            "password": "password123",
        },
    )

    assert second_response.status_code in (400, 409)


def test_register_missing_password():
    unique = uuid4().hex[:8]

    response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": f"{unique}@example.com",
        },
    )

    assert response.status_code == 422


def test_get_current_user_without_token():
    response = client.get("/auth/me")

    assert response.status_code == 401


def test_get_current_user_with_invalid_token():
    response = client.get(
        "/auth/me",
        headers={"Authorization": "Bearer invalid-token"},
    )

    assert response.status_code == 401


def test_get_current_user_with_malformed_auth_header():
    response = client.get(
        "/auth/me",
        headers={"Authorization": "InvalidToken"},
    )

    assert response.status_code == 401


def test_refresh_token():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
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

    refresh_token = login_response.json()["refresh_token"]

    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


def test_refresh_token_invalid():
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": "invalid-refresh-token",
        },
    )

    assert response.status_code == 401


def test_logout(client, auth_token):
    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Logged out successfully."


def test_logout_without_token(client):
    response = client.post("/auth/logout")

    assert response.status_code == 401


def test_forgot_password(client):
    unique = uuid4().hex[:8]

    email = f"{unique}@example.com"

    register_response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": email,
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": email,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "If an account with that email exists, a password reset link has been sent."
    )


def test_logout_after_login():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
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

    access_token = login_response.json()["access_token"]

    response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Logged out successfully."


def test_refresh_token_after_logout():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
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

    tokens = login_response.json()

    access_token = tokens["access_token"]
    refresh_token = tokens["refresh_token"]

    logout_response = client.post(
        "/auth/logout",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert logout_response.status_code == 200

    refresh_response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert refresh_response.status_code == 401


def test_register_duplicate_email():
    unique = uuid4().hex[:8]

    email = f"{unique}@example.com"

    first_response = client.post(
        "/auth/register",
        json={
            "username": f"user_{unique}",
            "email": email,
            "password": "password123",
        },
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/auth/register",
        json={
            "username": f"another_user_{unique}",
            "email": email,
            "password": "password123",
        },
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["success"] is False
    assert data["message"] == "Email already exists"
    assert data["data"] is None


def test_refresh_token_user_not_found():
    unique = uuid4().hex[:8]

    username = f"deleted_user_{unique}"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": f"{unique}@example.com",
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    # Login user
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": "password123",
        },
    )

    assert login_response.status_code == 200

    refresh_token = login_response.json()["refresh_token"]

    # Delete user directly from database
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        assert user is not None

        db.delete(user)
        db.commit()
    finally:
        db.close()

    # Try using refresh token after user was deleted
    response = client.post(
        "/auth/refresh",
        json={
            "refresh_token": refresh_token,
        },
    )

    assert response.status_code == 401
    assert response.json()["message"] == "User not found"


def test_forgot_password_nonexistent_email():
    unique = uuid4().hex[:8]

    response = client.post(
        "/auth/forgot-password",
        json={
            "email": f"nonexistent_{unique}@example.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["message"]
        == "If an account with that email exists, a password reset link has been sent."
    )


def test_reset_password_invalid_token():
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "invalid-reset-token",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["message"] == "Invalid or expired reset token."


def test_reset_password_expired_token():
    unique = uuid4().hex[:8]

    username = f"reset_user_{unique}"
    email = f"{unique}@example.com"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    # Directly put an expired reset token into the database
    from datetime import datetime, timedelta, timezone

    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        assert user is not None

        user.reset_token = "expired-test-token"
        user.reset_token_expires = datetime.now(timezone.utc) - timedelta(minutes=5)

        db.commit()
    finally:
        db.close()

    # Try to reset password using the expired token
    response = client.post(
        "/auth/reset-password",
        json={
            "token": "expired-test-token",
            "new_password": "newpassword123",
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["message"] == "Reset token has expired."


def test_reset_password_success():
    unique = uuid4().hex[:8]

    username = f"reset_success_{unique}"
    email = f"{unique}@example.com"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": "password123",
        },
    )

    assert register_response.status_code == 201

    # Create a valid reset token directly in the database
    from datetime import datetime, timedelta, timezone

    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        assert user is not None

        reset_token = f"valid-reset-token-{unique}"
        user.reset_token = reset_token
        user.reset_token_expires = datetime.now(timezone.utc) + timedelta(minutes=10)

        db.commit()
    finally:
        db.close()

    # Reset password
    response = client.post(
        "/auth/reset-password",
        json={
            "token": reset_token,
            "new_password": "newpassword123",
        },
    )
    assert response.status_code == 200

    data = response.json()

    assert data["message"] == "Password has been reset successfully."


def test_admin_dashboard():
    unique = uuid4().hex[:8]

    username = f"admin_{unique}"
    email = f"{unique}@example.com"
    password = "password123"

    # Register user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # Change user role to admin directly in database
    from app.database import SessionLocal
    from app.models.user import User

    db = SessionLocal()

    try:
        user = db.query(User).filter(User.username == username).first()

        assert user is not None

        user.role = "admin"
        db.commit()
        db.refresh(user)
        print("RESET TOKEN:", user.reset_token)
        print("RESET EXPIRY:", user.reset_token_expires)
        print("CURRENT UTC:", datetime.now(timezone.utc))
    finally:
        db.close()

    # Login as admin
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Access admin dashboard
    response = client.get(
        "/auth/admin",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["message"] == f"Welcome Admin {username}!"


def test_admin_dashboard_non_admin():
    unique = uuid4().hex[:8]

    username = f"user_{unique}"
    email = f"{unique}@example.com"
    password = "password123"

    # Register normal user
    register_response = client.post(
        "/auth/register",
        json={
            "username": username,
            "email": email,
            "password": password,
        },
    )

    assert register_response.status_code == 201

    # Login
    login_response = client.post(
        "/auth/login",
        data={
            "username": username,
            "password": password,
        },
    )

    assert login_response.status_code == 200

    access_token = login_response.json()["access_token"]

    # Normal user should NOT access admin dashboard
    response = client.get(
        "/auth/admin",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 403

    data = response.json()

    assert data["message"] == "Admin access required."
