import pytest


@pytest.mark.asyncio
async def test_create_product_success(client, auth_cookie):
    payload = {
        "title": "Test Product",
        "description": "Test Description",
        "price": 100,
        "quantity": 10,
    }

    response = await client.post(
        "/api/v1/products/",
        json=payload,
        cookies=auth_cookie,
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Product created successfully"


@pytest.mark.asyncio
async def test_create_product_negative_price(client, auth_cookie):
    payload = {
        "title": "Bad Product",
        "description": "Bad",
        "price": -10,
        "quantity": 5,
    }

    response = await client.post(
        "/api/v1/products/",
        json=payload,
        cookies=auth_cookie,
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_get_products(client):
    response = await client.get("/api/v1/products/")
    assert response.status_code == 200
    assert "products" in response.json()


@pytest.mark.asyncio
async def test_get_product_by_id_not_found(client):
    response = await client.get("/api/v1/products/9999")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_delete_product_unauthorized(client):
    response = await client.delete("/api/v1/products/Test Product")
    assert response.status_code == 400  # у тебя оборачивается в 400


@pytest.mark.asyncio
async def test_update_product_success(client, auth_cookie):
    # сначала создаем продукт
    payload = {
        "title": "Update Product",
        "description": "Desc",
        "price": 50,
        "quantity": 5,
    }

    await client.post(
        "/api/v1/products/",
        json=payload,
        cookies=auth_cookie,
    )

    update_payload = {
        "title": "Updated",
        "description": "Updated Desc",
        "price": 60,
        "quantity": 10,
    }

    response = await client.put(
        "/api/v1/products/1",
        json=update_payload,
        cookies=auth_cookie,
    )

    assert response.status_code == 200
