import json
from decimal import Decimal

from fastapi import APIRouter, HTTPException, status, Response, Cookie
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import ProductModel
from src.database.queries import (
    create_products_query,
    update_product_query,
    delete_product_query,
    get_product_by_id_from_db_query,
    get_all_products_from_db_query,
)
from src.database.connect import engine
from src.schemas.schemas import CreateProductSchema, UpdateProductSchema
from src.utils.auth import config

router_v1 = APIRouter(prefix="/api/v1/products", tags=["products v1"])
router_v2 = APIRouter(prefix="/api/v2/products", tags=["products v2"])


@router_v1.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    product: CreateProductSchema,
    authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
):
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")

    if product.price < 0:
        raise HTTPException(status_code=400, detail="Price cannot be negative")

    if product.quantity < 0:
        raise HTTPException(
            status_code=400, detail="Quantity cannot be negative"
        )

    await create_products_query(product=product)

    return {
        "message": "Product created successfully",
        "status": status.HTTP_201_CREATED,
    }


@router_v1.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_product_by_id(product_id: int):
    try:
        product = await get_product_by_id_from_db_query(product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product
    except HTTPException:
        raise


@router_v1.get("/", status_code=status.HTTP_200_OK)
async def get_products():
    products = await get_all_products_from_db_query()
    return Response(
        content=json.dumps({"products": products}),
        media_type="application/json",
        headers={"cache-control": "max-age=3600"},
    )


@router_v1.delete("/{product_title}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_title: str,
    authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
):
    # if not authorization:
    #     raise HTTPException(status_code=401, detail="Invalid credentials")
    result = await delete_product_query(product_name=product_title)
    if not result:
        raise HTTPException(status_code=404, detail="Product not found")
    return Response(status_code=204)


@router_v1.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    product_id: int,
    update: UpdateProductSchema,
    authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
):
    """Обновление товара
    - **title**: Название товара
    - **description**: Описание товара
    - **price**: Стоимость товара
    - **quantity**: Наличие на складе
    - Необходимо передать весь json
    - **Необходима авторизация через http://0.0.0.0:8000/api/v1/users/login**
    """
    async with AsyncSession(engine) as conn:
        try:
            if not authorization:
                raise HTTPException(
                    status_code=401, detail="Invalid credentials"
                )
            result = await conn.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product = result.scalars().first()
            if not product:
                raise HTTPException(
                    status_code=404, detail=f"Product {product_id} not found"
                )
            if (
                not update.title
                or not update.description
                or not update.price
                or not update.quantity
            ):
                raise HTTPException(
                    status_code=400, detail="Missing parameters"
                )

            product.title = update.title
            product.quantity = update.quantity
            product.price = Decimal(update.price)
            product.description = update.description

            await conn.commit()
            await conn.refresh(product)
            return {"message": "Product updated successfully"}
        except HTTPException as e:
            raise e


@router_v2.patch("/{product_name}", status_code=status.HTTP_200_OK)
async def update_product(
    product_name: str,
    product: UpdateProductSchema,
    authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
):
    """Обновление товара в базе данных по названию товара
    - **title**: название товара
    - **description**: описание товара
    - **price**: стоимость товара
    - **quantity**: наличие на складе
    данные не переданные в json не будут изменены
    - **Необходима авторизация через http://0.0.0.0:8000/api/v1/users/login**
    """
    try:
        if not authorization:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        await update_product_query(product_name=product_name, update=product)
        return {
            "message": f"Product updated {product_name} successfully",
            "status_code": status.HTTP_200_OK,
            "metadata": {
                "product_name": product_name,
                "product_description": product.description,
                "product_price": product.price,
                "product_quantity": product.quantity,
            },
        }
    except HTTPException as e:
        raise HTTPException(
            status_code=400, detail=f"Something went wrong: {e}"
        )
