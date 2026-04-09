import pytest
from unittest.mock import AsyncMock, patch


@pytest.mark.asyncio
@patch(
    "src.api.handlers.products.create_products_query", new_callable=AsyncMock
)
async def test_create_product_success(mock_create, client):
    response = await client.post(
        "/api/v1/products/",
        json={
            "title": "Test",
            "description": "Desc",
            "price": 10,
            "quantity": 5,
        },
        cookies={"access_token": "fake"},
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Product created successfully"
    mock_create.assert_awaited_once()


# @pytest.mark.asyncio
# async def test_create_product_no_auth(client):
#     response = await client.post(
#         "/api/v1/products/",
#         json={
#             "title": "Test",
#             "description": "Desc",
#             "price": 10,
#             "quantity": 5,
#         },
#     )
#
#     assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_product_negative_price(client):
    response = await client.post(
        "/api/v1/products/",
        json={
            "title": "Test",
            "description": "Desc",
            "price": -1,
            "quantity": 5,
        },
        cookies={"access_token": "fake"},
    )

    assert response.status_code == 400


@pytest.mark.asyncio
@patch(
    "src.api.handlers.products.get_product_by_id_from_db_query",
    new_callable=AsyncMock,
)
async def test_get_product_by_id_success(mock_get, client):
    mock_get.return_value = {"id": 1, "title": "Test"}

    response = await client.get("/api/v1/products/1")

    assert response.status_code == 200
    assert response.json()["title"] == "Test"


@pytest.mark.asyncio
@patch(
    "src.api.handlers.products.get_product_by_id_from_db_query",
    new_callable=AsyncMock,
)
async def test_get_product_by_id_not_found(mock_get, client):
    mock_get.return_value = None

    response = await client.get("/api/v1/products/999")

    assert response.status_code == 404


@pytest.mark.asyncio
@patch(
    "src.api.handlers.products.get_all_products_from_db_query",
    new_callable=AsyncMock,
)
async def test_get_products(mock_get_all, client):
    mock_get_all.return_value = [{"id": 1}]

    response = await client.get("/api/v1/products/")

    assert response.status_code == 200
    assert "products" in response.json()


@pytest.mark.asyncio
@patch(
    "src.api.handlers.products.delete_product_query", new_callable=AsyncMock
)
async def test_delete_product_success(mock_delete, client):
    mock_delete.return_value = True

    response = await client.delete(
        "/api/v1/products/Test",
        cookies={"access_token": "fake"},
    )

    assert response.status_code == 204


@pytest.mark.asyncio
@patch(
    "src.api.handlers.products.delete_product_query", new_callable=AsyncMock
)
async def test_delete_product_not_found(mock_delete, client):
    mock_delete.return_value = False

    response = await client.delete(
        "/api/v1/products/Test",
        cookies={"access_token": "fake"},
    )

    assert response.status_code == 404  # из-за try/except в коде


# @pytest.mark.asyncio
# async def test_delete_product_no_auth(client):
#     response = await client.delete("/api/v1/products/Test")
#
#     assert response.status_code == 400  # тоже оборачивается в 400
