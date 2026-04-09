import pytest


@pytest.mark.asyncio
async def test_login_success(client):
    response = await client.post(
        "/api/v1/users/login",
        json={"username": "test", "password": "test"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_fail(client):
    response = await client.post(
        "/api/v1/users/login",
        json={"username": "wrong", "password": "wrong"},
    )
    assert response.status_code == 401
