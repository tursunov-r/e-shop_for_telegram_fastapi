from decimal import Decimal

from sqlalchemy import select

from src.core.db_connect import create_session
from src.database.models import ProductModel
from product_service.schemas.schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)


async def create_products_query(
    product: CreateProductSchema,
):
    async with create_session() as session:
        try:
            product = ProductModel(
                title=product.title,
                quantity=product.quantity,
                price=Decimal(product.price),
                description=product.description,
            )
            session.add(product)
            await session.commit()
            await session.refresh(product)
            return product
        except Exception as e:
            await session.rollback()
            raise e


async def update_product_in_db_query(product_id, data):
    async with create_session() as session:
        try:
            result = await session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product = result.scalar_one_or_none()
            if not product:
                raise ValueError(f"Product {product_id} not found")

            product.title = data["title"]
            product.quantity = data["quantity"]
            product.price = data["price"]
            product.description = data["description"]

            await session.commit()
            await session.refresh(product)
            return product
        except Exception as e:
            await session.rollback()
            raise e


async def get_all_products_from_db_query():
    async with create_session() as session:
        result = await session.execute(select(ProductModel))
        products = result.scalars().all()
        return [
            {
                "id": product.id,
                "title": product.title,
                "quantity": product.quantity,
                "price": float(product.price),
            }
            for product in products
        ]


async def get_product_by_id_from_db_query(product_id: int):
    async with create_session() as session:
        result = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = result.scalar_one_or_none()
        return product


async def update_product_query(product_name: str, update: UpdateProductSchema):
    async with create_session() as session:
        result = await session.execute(
            select(ProductModel).where(ProductModel.title == product_name)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError(f"Product {product_name} not found")

        # Обновляем только непустые поля
        if update.title is not None:
            product.title = update.title
        if update.quantity is not None:
            product.quantity = update.quantity
        if update.price is not None:
            product.price = Decimal(update.price)
        if update.description is not None:
            product.description = update.description

        await session.commit()
        await session.refresh(product)
        return product


async def delete_product_query(product_name: str):
    async with create_session() as session:
        result = await session.execute(
            select(ProductModel).where(ProductModel.title == product_name)
        )
        product = result.scalar_one_or_none()
        if not product:
            return None
        await session.delete(product)
        await session.commit()
        return {"message": "Product deleted"}
