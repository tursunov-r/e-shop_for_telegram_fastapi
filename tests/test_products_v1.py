import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from src.core.settings import settings
from src.main import app

barcode = "2827101152234"
title = "test product".title().strip()
description = "the best test product"
price = 100
purchase_price = 20.00
quantity = 10.00
lang_code = "en"
product_id = None  # глобальная переменная


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c


@pytest_asyncio.fixture
async def auth_token(client):
    response = await client.post(
        "/api/v1/users/login",
        json={
            "email": settings.admin_email,
            "password": settings.admin_password,
        },
    )
    assert response.status_code == 200
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_create_product(client, auth_token):
    response = await client.post(
        "/api/v1/products/",
        json={
            "barcode": barcode,
            "price": price,
            "purchase_price": purchase_price,
            "stock": quantity,
            "translate": [
                {
                    "lang_code": lang_code,
                    "title": title,
                    "description": description,
                }
            ],
            "archived": False,
        },
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 201


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
                if any(t["title"] == title for t in item["translate"])
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

        assert data["id"] == product_id
        assert data["price"] == str(price)
        assert data["quantity"] == quantity
        assert data["barcode"] == str(barcode)
        assert data["archived"] is False

        # проверка перевода
        assert any(t["title"] == title for t in data["translate"])


@pytest.mark.asyncio
async def test_get_product_by_name():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

        response = await client.get(f"/api/v1/products/search/{title}")
        assert response.status_code == 200

        data = response.json()

        assert len(data) >= 1

        product = data[0]

        assert product["id"] == product_id
        assert product["barcode"] == str(barcode)
        assert product["price"] == str(price)
        assert product["purchase_price"] == str(purchase_price)
        assert product["quantity"] == quantity
        assert product["archived"] is False

        assert any(t["title"] == title for t in product["translate"])


@pytest.mark.asyncio
async def test_get_product_by_barcode():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

        response = await client.get(f"/api/v1/products/search/{barcode}")
        assert response.status_code == 200

        data = response.json()

        assert len(data) >= 1

        product = data[0]

        assert product["id"] == product_id
        assert product["barcode"] == str(barcode)
        assert product["price"] == str(price)
        assert product["purchase_price"] == str(purchase_price)
        assert product["quantity"] == quantity
        assert product["archived"] is False

        assert any(t["title"] == title for t in product["translate"])


@pytest.mark.asyncio
async def test_update_product(client, auth_token):
    response = await client.patch(
        f"/api/v1/products/{barcode}",
        json={"price": 1000},
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 200
    data = response.json()

    assert data["id"] == product_id
    assert data["price"] == str(1000)
    assert data["quantity"] == quantity
    assert any(t["title"] == title for t in data["translate"])


@pytest.mark.asyncio
async def test_delete_product(client, auth_token):
    response = await client.delete(
        f"/api/v1/products/barcode/{barcode}",
        headers={"Authorization": f"Bearer {auth_token}"},
    )

    assert response.status_code == 204
