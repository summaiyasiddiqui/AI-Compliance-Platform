from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app
from app.services import company_service


def test_create_company(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Test Company {unique}",
            "industry": "Technology",
            "email": f"{unique}@company.com",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Company created successfully!"
    assert data["data"]["company_name"] == f"Test Company {unique}"
    assert data["data"]["industry"] == "Technology"
    assert data["data"]["email"] == f"{unique}@company.com"

def test_create_company_database_failure(client, auth_token, monkeypatch):
    def mock_create_company(*args, **kwargs):
        raise RuntimeError("Database connection failed")

    monkeypatch.setattr(
        company_service,
        "create_company",
        mock_create_company,
    )

    test_client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = test_client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "company_name": "Database Failure Test",
            "industry": "Technology",
            "email": "dbfailure@example.com",
        },
    )

    assert response.status_code == 500

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "An internal server error occurred."
    assert data["data"] is None

    assert "Database connection failed" not in response.text

def test_get_companies(client, auth_token):
    token = auth_token

    response = client.get(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "companies" in data["data"]
    assert "meta" in data["data"]


def test_get_companies_with_search(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Searchable Company {unique}",
            "industry": "Technology",
            "email": f"{unique}@search.com",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        params={"search": "Searchable"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["data"]["companies"]) >= 1
    assert any(
        "Searchable Company" in company["company_name"]
        for company in data["data"]["companies"]
    )


def test_get_companies_with_industry_filter(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Healthcare Company {unique}",
            "industry": "Healthcare",
            "email": f"{unique}@healthcare.com",
        },
    )

    assert create_response.status_code == 201

    response = client.get(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        params={"industry": "Healthcare"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert len(data["data"]["companies"]) >= 1
    assert all(
        company["industry"] == "Healthcare" for company in data["data"]["companies"]
    )


def test_get_companies_descending_sort(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    for name in [
        f"Alpha Company {unique}",
        f"Beta Company {unique}",
    ]:
        response = client.post(
            "/companies/",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "company_name": name,
                "industry": "Technology",
                "email": f"{uuid4().hex[:8]}@sort.com",
            },
        )

        assert response.status_code == 201

    response = client.get(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        params={
            "sort_by": "company_name",
            "order": "desc",
        },
    )

    assert response.status_code == 200

    data = response.json()
    companies = data["data"]["companies"]

    names = [company["company_name"] for company in companies]

    assert names == sorted(names, reverse=True)


def test_get_company_by_id(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Get Test {unique}",
            "industry": "Technology",
            "email": f"{unique}@gettest.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    response = client.get(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == company_id
    assert data["company_name"] == f"Get Test {unique}"


def test_create_company_without_token(client):
    unique = uuid4().hex[:8]

    response = client.post(
        "/companies/",
        json={
            "company_name": f"Unauthorized {unique}",
            "industry": "Technology",
            "email": f"{unique}@unauthorized.com",
        },
    )

    assert response.status_code == 401


def test_get_companies_without_token(client):
    response = client.get("/companies/")

    assert response.status_code == 401


def test_create_company_missing_field(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Invalid Company {unique}",
            "industry": "Technology",
        },
    )

    assert response.status_code == 422


def test_get_nonexistent_company(client, auth_token):
    token = auth_token

    response = client.get(
        "/companies/999999",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 404


def test_update_company(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Update Test {unique}",
            "industry": "Technology",
            "email": f"{unique}@update.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    response = client.put(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Updated Company {unique}",
            "industry": "Healthcare",
            "email": f"{unique}@updated.com",
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Company updated successfully!"
    assert data["data"]["company_name"] == f"Updated Company {unique}"
    assert data["data"]["industry"] == "Healthcare"
    assert data["data"]["email"] == f"{unique}@updated.com"


def test_delete_company(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": f"Delete Test {unique}",
            "industry": "Technology",
            "email": f"{unique}@delete.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    response = client.delete(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert data["message"] == "Company deleted successfully!"
    assert data["data"] is None


def test_delete_company_without_token(client):
    response = client.delete("/companies/999999")

    assert response.status_code == 401


def test_update_company_without_token(client):
    response = client.put(
        "/companies/999999",
        json={
            "company_name": "Unauthorized Update",
            "industry": "Technology",
            "email": "unauthorized@update.com",
        },
    )

    assert response.status_code == 401


def test_update_nonexistent_company(client, auth_token):
    token = auth_token

    response = client.put(
        "/companies/999999",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "company_name": "Nonexistent Update",
            "industry": "Technology",
            "email": "nonexistent@update.com",
        },
    )

    assert response.status_code == 404


def test_get_company_unauthorized_owner(client, auth_token):
    owner_token = auth_token
    unique = uuid4().hex[:8]

    # Owner creates the company
    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "company_name": f"Private Company {unique}",
            "industry": "Technology",
            "email": f"{unique}@private.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    # Create a second user
    other_unique = uuid4().hex[:8]

    register_response = client.post(
        "/auth/register",
        json={
            "username": f"other_user_{other_unique}",
            "email": f"{other_unique}@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": f"other_user_{other_unique}",
            "password": "StrongPassword123",
        },
    )

    assert login_response.status_code == 200

    other_token = login_response.json()["access_token"]

    # Other user tries to access the company
    response = client.get(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 404


def test_create_duplicate_company(client, auth_token):
    token = auth_token
    unique = uuid4().hex[:8]

    company_data = {
        "company_name": f"Duplicate Company {unique}",
        "industry": "Technology",
        "email": f"{unique}@duplicate.com",
    }

    first_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json=company_data,
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {token}"},
        json=company_data,
    )

    assert second_response.status_code == 400

    data = second_response.json()

    assert data["success"] is False
    assert data["message"] == "You already have a company with this name."
    assert data["data"] is None


def test_update_company_unauthorized_owner(client, auth_token):
    owner_token = auth_token
    unique = uuid4().hex[:8]

    # Owner creates the company
    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "company_name": f"Protected Company {unique}",
            "industry": "Technology",
            "email": f"{unique}@protected.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    # Create second user
    other_unique = uuid4().hex[:8]

    register_response = client.post(
        "/auth/register",
        json={
            "username": f"other_update_{other_unique}",
            "email": f"{other_unique}@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": f"other_update_{other_unique}",
            "password": "StrongPassword123",
        },
    )

    assert login_response.status_code == 200

    other_token = login_response.json()["access_token"]

    # Other user tries to update the company
    response = client.put(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {other_token}"},
        json={
            "company_name": f"Hacked Company {unique}",
            "industry": "Healthcare",
            "email": f"{unique}@hacked.com",
        },
    )

    assert response.status_code == 404


def test_delete_company_unauthorized_owner(client, auth_token):
    owner_token = auth_token
    unique = uuid4().hex[:8]

    # Owner creates the company
    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "company_name": f"Protected Delete {unique}",
            "industry": "Technology",
            "email": f"{unique}@delete.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    # Create second user
    other_unique = uuid4().hex[:8]

    register_response = client.post(
        "/auth/register",
        json={
            "username": f"other_delete_{other_unique}",
            "email": f"{other_unique}@example.com",
            "password": "StrongPassword123",
        },
    )

    assert register_response.status_code == 201

    login_response = client.post(
        "/auth/login",
        data={
            "username": f"other_delete_{other_unique}",
            "password": "StrongPassword123",
        },
    )

    assert login_response.status_code == 200

    other_token = login_response.json()["access_token"]

    # Other user tries to delete the company
    response = client.delete(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert response.status_code == 404


def test_delete_nonexistent_company(client, auth_token):
    response = client.delete(
        "/companies/999999",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 403
    assert (
        response.json()["message"] == "You are not authorized to delete this company."
    )
def test_get_companies_invalid_page(client, auth_token):
    response = client.get(
        "/companies/?page=0",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 422


def test_get_companies_negative_page(client, auth_token):
    response = client.get(
        "/companies/?page=-1",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 422


def test_get_companies_invalid_limit_zero(client, auth_token):
    response = client.get(
        "/companies/?limit=0",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 422


def test_get_companies_limit_above_maximum(client, auth_token):
    response = client.get(
        "/companies/?limit=101",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 422


def test_get_companies_invalid_order(client, auth_token):
    response = client.get(
        "/companies/?order=invalid",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 422


def test_get_companies_empty_page(client, auth_token):
    response = client.get(
        "/companies/?page=9999",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200

    data = response.json()["data"]

    assert data["companies"] == []
    assert data["meta"]["current_page"] == 9999

def test_update_company_database_failure(client, auth_token, monkeypatch):
    unique = uuid4().hex[:8]

    create_response = client.post(
        "/companies/",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "company_name": f"Update Failure {unique}",
            "industry": "Technology",
            "email": f"{unique}@company.com",
        },
    )

    assert create_response.status_code == 201

    company_id = create_response.json()["data"]["id"]

    def mock_update_company(*args, **kwargs):
        raise RuntimeError("Database update failed")

    monkeypatch.setattr(
        company_service,
        "update_company",
        mock_update_company,
    )

    test_client = TestClient(
        app,
        raise_server_exceptions=False,
    )

    response = test_client.put(
        f"/companies/{company_id}",
        headers={"Authorization": f"Bearer {auth_token}"},
        json={
            "company_name": f"Updated Company {unique}",
            "industry": "Finance",
            "email": f"updated_{unique}@company.com",
        },
    )

    assert response.status_code == 500

    data = response.json()

    assert data["success"] is False
    assert data["message"] == "An internal server error occurred."
    assert data["data"] is None

    assert "Database update failed" not in response.text

def test_company_list_isolated_between_users(client):
    unique_a = uuid4().hex[:8]
    unique_b = uuid4().hex[:8]

    user_a = {
        "username": f"user_a_{unique_a}",
        "email": f"user_a_{unique_a}@example.com",
        "password": "StrongPassword123",
    }

    user_b = {
        "username": f"user_b_{unique_b}",
        "email": f"user_b_{unique_b}@example.com",
        "password": "StrongPassword123",
    }

    response_a = client.post("/auth/register", json=user_a)
    response_b = client.post("/auth/register", json=user_b)

    assert response_a.status_code == 201
    assert response_b.status_code == 201

    login_a = client.post(
        "/auth/login",
        data={
            "username": user_a["username"],
            "password": user_a["password"],
        },
    )

    login_b = client.post(
        "/auth/login",
        data={
            "username": user_b["username"],
            "password": user_b["password"],
        },
    )

    assert login_a.status_code == 200
    assert login_b.status_code == 200

    token_a = login_a.json()["access_token"]
    token_b = login_b.json()["access_token"]

    company_response = client.post(
        "/companies/",
        json={
            "company_name": f"User A Company {unique_a}",
            "industry": "Technology",
            "email": f"company_{unique_a}@example.com",
            "website": "https://example.com",
        },
        headers={"Authorization": f"Bearer {token_a}"},
    )

    assert company_response.status_code == 201

    response_b = client.get(
        "/companies/",
        headers={"Authorization": f"Bearer {token_b}"},
    )

    assert response_b.status_code == 200

    companies = response_b.json()["data"]["companies"]

    assert all(
        company["company_name"] != f"User A Company {unique_a}"
        for company in companies
    )