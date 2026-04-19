from decimal import Decimal

from fastapi import Response, HTTPException, Cookie, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)
from src.utils.auth import config
from src.repositories.product_repository import ProductRepository

product_repo = ProductRepository()


class ProductService:
    @staticmethod
    async def create_product(
        product: CreateProductSchema,
        session: AsyncSession,
        authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
    ):
        if not authorization:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        create = await product_repo.create_products_query(
            product=product, session=session
        )

        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={"message": "success"},
        )

    @staticmethod
    async def update_product(
        product_name: str,
        product: UpdateProductSchema,
        session: AsyncSession,
        authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
    ):
        if not authorization:
            raise HTTPException(status_code=401, detail="Unauthorized")
        update = await product_repo.update_product_query(
            product_name=product_name, update=product, session=session
        )
        if update:
            return update
        raise HTTPException(status_code=400, detail=f"Something went wrong")

    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession):
        product = await product_repo.get_product_by_id_from_db_query(
            product_id=product_id, session=session
        )
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return product

    @staticmethod
    async def get_products(session: AsyncSession):
        products = await product_repo.get_all_products_from_db_query(
            session=session
        )
        return products

    @staticmethod
    async def search_products(
        title: str,
        min_price: Decimal,
        max_price: Decimal,
        session: AsyncSession,
    ):
        result = await product_repo.search_product(
            title=title,
            min_price=min_price,
            max_price=max_price,
            session=session,
        )
        return result

    @staticmethod
    async def delete_product(
        session: AsyncSession,
        product_title: str,
        authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
    ):
        if not authorization:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        result = await product_repo.delete_product_query(
            product_name=product_title, session=session
        )
        if not result:
            raise HTTPException(status_code=404, detail="Product not found")
        return Response(status_code=204)
