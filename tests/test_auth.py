import pytest
from httpx import AsyncClient, ASGITransport

from src.main import app

user_email = "user_1_@example.com"
password = "stringsT1!"
confirm_password = "stringsT1!"


@pytest.mark.asyncio
async def test_create_user_success():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/users/",
            json={
                "first_name": "string",
                "last_name": "string",
                "email": f"{user_email}",
                "password": f"{password}",
                "confirm_password": f"{confirm_password}",
                "balance": 0,
            },
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_email_already_exists():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/users/",
            json={
                "first_name": "string",
                "last_name": "string",
                "email": f"{user_email}",
                "password": f"{password}",
                "confirm_password": f"{confirm_password}",
                "balance": 0,
            },
        )
        assert response.status_code == 400
        data = response.json()
        assert len(data) == 1
        assert data == {"detail": "Email already registered"}


@pytest.mark.asyncio
async def test_create_user_failure():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/users/",
            json={
                "first_name": "string",
                "last_name": "string",
                "email": f"{user_email}1",
                "password": f"{password.lower()}",
                "confirm_password": f"{confirm_password.lower()}",
                "balance": 0,
            },
        )
        assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post(
        "/api/v1/users/login",
        json={"email": f"{user_email}", "password": f"{password}"},
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_login_fail(client):
    response = await client.post(
        "/api/v1/users/login",
        json={"email": f"{user_email}", "password": f"{password.lower()}"},
    )
    assert response.status_code == 401
    data = response.json()
    print(data)
    assert len(data) == 1
    assert data == {"detail": "Invalid credentials"}


@pytest.mark.asyncio
async def test_delete_user_success():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.request(
            "DELETE",
            "/api/v1/users/",
            json={"email": user_email, "password": password},
        )
        assert response.status_code == 204


@pytest.mark.asyncio
async def test_delete_user_failure():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.request(
            "DELETE",
            "/api/v1/users/",
            json={"email": f"1{user_email}", "password": password},
        )
        assert response.status_code == 404
