from decimal import Decimal

from fastapi import Response, HTTPException, Cookie, status
from starlette.responses import JSONResponse

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
    SearchProductSchema,
)
from src.utils.auth import config
from src.repositories.product_repository import ProductRepository

product_repo = ProductRepository()


class ProductService:
    @staticmethod
    async def create_product(
        product: CreateProductSchema,
        authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
    ):
        if not authorization:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        create = await product_repo.create_products_query(product=product)

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "success"},
        )

    @staticmethod
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
                raise HTTPException(
                    status_code=401, detail="Invalid credentials"
                )
            update = await product_repo.update_product_query(
                product_name=product_name, update=product
            )
            return JSONResponse(
                content=update,
                media_type="application/json",
                status_code=status.HTTP_200_OK,
                headers={"content-type": "application/json"},
            )
        except HTTPException as e:
            raise HTTPException(
                status_code=400, detail=f"Something went wrong: {e}"
            )

    @staticmethod
    async def get_product_by_id(product_id: int):
        product = await product_repo.get_product_by_id_from_db_query(
            product_id
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    async def get_products():
        products = await product_repo.get_all_products_from_db_query()
        return JSONResponse(
            content={"products": products},
            media_type="application/json",
            headers={"cache-control": "max-age=3600"},
        )

    @staticmethod
    async def search_products(
        title: str, min_price: Decimal, max_price: Decimal
    ):
        result = await product_repo.search_product(
            title=title, min_price=min_price, max_price=max_price
        )
        return {"products": result}

    @staticmethod
    async def delete_product(
        product_title: str,
        authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
    ):
        if not authorization:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        result = await product_repo.delete_product_query(
            product_name=product_title
        )
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        return Response(status_code=204)
