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


def test_unhandled_exception_returns_safe_500():
    @app.get("/test-unhandled-error")
    async def test_unhandled_error():
        raise RuntimeError("Sensitive internal error")

    try:
        test_client = TestClient(app, raise_server_exceptions=False)

        response = test_client.get("/test-unhandled-error")

        assert response.status_code == 500

        data = response.json()

        assert data["success"] is False
        assert data["message"] == "An internal server error occurred."
        assert data["data"] is None

        assert "Sensitive internal error" not in response.text

    finally:
        app.routes[:] = [
            route
            for route in app.routes
            if getattr(route, "path", None) != "/test-unhandled-error"
        ]