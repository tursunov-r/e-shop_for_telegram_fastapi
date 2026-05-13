from decimal import Decimal

from fastapi import Response, Cookie, status
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)
from src.utils.auth import config
from src.repositories.product_repository import product_repository
from src.utils.exceptions.exceptions import NotAuthorized


class ProductService:
    @staticmethod
    async def create_product(
        product: CreateProductSchema,
        session: AsyncSession,
        authorization: str = Cookie(None, alias=config.JWT_ACCESS_COOKIE_NAME),
    ):
        if not authorization:
            raise NotAuthorized("Not authorized")
        await product_repository.create_products_query(
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
            raise NotAuthorized("Not authorized")
        update = await product_repository.update_product_query(
            product_name=product_name, update=product, session=session
        )
        if update:
            return update
        raise ValueError("Something went wrong")

    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession):
        product = await product_repository.get_product_by_id_from_db_query(
            product_id=product_id, session=session
        )
        if not product:
            raise ValueError("Product not found")
        return product

    @staticmethod
    async def get_products(session: AsyncSession):
        products = await product_repository.get_all_products_from_db_query(
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
        result = await product_repository.search_product(
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
            raise NotAuthorized("Not authorized")
        result = await product_repository.delete_product_query(
            product_name=product_title, session=session
        )
        if not result:
            raise ValueError("Product not found")
        return Response(status_code=204)

    @staticmethod
    async def delete_product_by_id(product_id: int, session: AsyncSession):
        await product_repository.delete_product_by_id_from_db_query(
            product_id=product_id, session=session
        )
        return Response(status_code=204)
