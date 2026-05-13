import pytest
from httpx import AsyncClient, ASGITransport
from src.main import app

title = "test product".title().strip()
description = "the best test product"
price = 100
quantity = 10
product_id = None  # глобальная переменная


@pytest.mark.asyncio
async def test_create_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/api/v1/products/",
            json={
                "title": title,
                "description": description,
                "price": price,
                "quantity": quantity,
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data == {"message": "created"}


@pytest.mark.asyncio
async def test_get_products():
    global product_id
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get("/api/v1/products/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        product_id = next(
            (
                item["id"]
                for item in data
                if item["title"] == title.title().strip()
            ),
            None,
        )
        print("product_id:", product_id)
        assert product_id is not None


@pytest.mark.asyncio
async def test_get_product_by_id():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(f"/api/v1/products/id/{product_id}")
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "id": product_id,
            "title": title,
            "price": str(price),
            "quantity": quantity,
            "description": description,
        }


@pytest.mark.asyncio
async def test_get_product_by_name():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.get(f"/api/v1/products/title/{title}")
        assert response.status_code == 200
        data = response.json()
        assert data == [
            {
                "id": product_id,
                "title": title,
                "price": str(price),
                "quantity": quantity,
                "description": description,
            }
        ]


@pytest.mark.asyncio
async def test_update_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.patch(
            f"/api/v1/products/{title}", json={"price": 1000}
        )
        assert response.status_code == 200
        data = response.json()
        assert data == {
            "id": product_id,
            "title": title,
            "price": str(1000),
            "quantity": quantity,
            "description": description,
        }


@pytest.mark.asyncio
async def test_delete_product():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.delete(f"/api/v1/products/title/{title}")
        assert response.status_code == 204
