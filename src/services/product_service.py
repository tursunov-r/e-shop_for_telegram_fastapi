from decimal import Decimal

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)
from src.repositories.product_repository import product_repository
from src.repositories.admin_permission import admin_permission
from src.schemas.user_schemas import TokenData


class ProductService:
    @staticmethod
    async def create_product(
        product: CreateProductSchema,
        session: AsyncSession,
        user: TokenData,
    ):
        await admin_permission.check_permission(session, user)
        new_product = await product_repository.create_products_query(
            product=product, session=session
        )

        return {"data": new_product}

    @staticmethod
    async def update_product(
        barcode: str,
        product: UpdateProductSchema,
        session: AsyncSession,
        user: TokenData,
    ):
        await admin_permission.check_permission(session, user)
        update = await product_repository.update_product_query(
            barcode=barcode, update=product, session=session
        )
        if update:
            return update
        raise ValueError("Something went wrong")

    @staticmethod
    async def get_product_by_id(product_id: int, session: AsyncSession):
        product = await product_repository.get_product_by_id_from_db_query(
            product_id=product_id, session=session
        )
        return product

    @staticmethod
    async def get_products(session: AsyncSession):
        products = await product_repository.get_all_products_from_db_query(
            session=session
        )
        return products

    @staticmethod
    async def search_products(
        search: str,
        session: AsyncSession,
        min_price: Decimal | None = None,
        max_price: Decimal | None = None,
    ):
        result = await product_repository.search_product(
            search=search.title().strip(),
            min_price=min_price,
            max_price=max_price,
            session=session,
        )
        return result

    @staticmethod
    async def delete_product(
        session: AsyncSession,
        barcode: str,
        user: TokenData,
    ):
        await admin_permission.check_permission(session, user)
        result = await product_repository.delete_product_query(
            barcode=barcode, session=session
        )
        if not result:
            raise ValueError("Product not found")
        return Response(status_code=204)

    @staticmethod
    async def delete_product_by_id(
        product_id: int, session: AsyncSession, user: TokenData
    ):
        await admin_permission.check_permission(session, user)
        await product_repository.delete_product_by_id_from_db_query(
            product_id=product_id, session=session
        )
        return Response(status_code=204)


product_service = ProductService()
