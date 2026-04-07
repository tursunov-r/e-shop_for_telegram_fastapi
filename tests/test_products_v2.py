import pytest


@pytest.mark.asyncio
async def test_patch_product_success(client, auth_cookie):
    # создаем продукт
    payload = {
        "title": "Patch Product",
        "description": "Desc",
        "price": 20,
        "quantity": 2,
    }

    await client.post(
        "/api/v1/products/",
        json=payload,
        cookies=auth_cookie,
    )

    update_payload = {
        "description": "New Desc",
        "price": 30,
    }

    response = await client.patch(
        "/api/v2/products/Patch Product",
        json=update_payload,
        cookies=auth_cookie,
    )

    assert response.status_code == 200
    assert response.json()["metadata"]["product_price"] == 30
