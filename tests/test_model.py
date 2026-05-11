import pytest

from httpx import AsyncClient, ASGITransport

from src.main import app


@pytest.mark.asyncio
async def test_create_order():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post(
            "api/v1/orders",
            json={
                {
                    "user_id": 0,
                    "product_ids": [{"product_id": 1, "quantity": 2}],
                }
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
