from decimal import Decimal

from sqlalchemy import select
from fastapi import HTTPException

from src.core.db_connect import create_session
from src.models.product_model import ProductModel
from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)


class ProductRepository:
    @staticmethod
    async def create_products_query(
        product: CreateProductSchema,
    ):
        async with create_session() as session:
            try:
                product = ProductModel(
                    title=product.title.title(),
                    quantity=product.quantity,
                    price=Decimal(product.price),
                    description=product.description,
                )
                session.add(product)
                await session.commit()
                await session.refresh(product)
                return product
            except:
                await session.rollback()
                raise HTTPException(
                    status_code=400, detail="Something went wrong"
                )

    @staticmethod
    async def get_all_products_from_db_query():
        async with create_session() as session:
            result = await session.execute(select(ProductModel))
            products = result.scalars().all()
            if products:
                return [
                    {
                        "id": product.id,
                        "title": product.title,
                        "quantity": product.quantity,
                        "price": float(product.price),
                    }
                    for product in products
                ]
            raise HTTPException(status_code=404, detail="No products yet")

    @staticmethod
    async def get_product_by_id_from_db_query(product_id: int):
        async with create_session() as session:
            result = await session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product = result.scalar_one_or_none()
            if product:
                return product
            raise HTTPException(status_code=404, detail="Product not found")

    @staticmethod
    async def search_product(
        title: str, min_price: Decimal, max_price: Decimal
    ):
        async with create_session() as session:
            print(title, min_price, max_price)
            result = await session.execute(
                select(ProductModel)
                .where(ProductModel.title.ilike(f"%{title}%"))
                .where(ProductModel.price.between(min_price, max_price))
            )
            products = result.scalars().all()
            if products:
                return products
            raise HTTPException(status_code=404, detail="No products yet")

    @staticmethod
    async def update_product_query(
        product_name: str, update: UpdateProductSchema
    ):
        async with create_session() as session:
            result = await session.execute(
                select(ProductModel).where(ProductModel.title == product_name)
            )
            product = result.scalar_one_or_none()
            if not product:
                raise HTTPException(
                    status_code=404, detail="Product not found"
                )

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

    @staticmethod
    async def delete_product_query(product_name: str):
        async with create_session() as session:
            result = await session.execute(
                select(ProductModel).where(ProductModel.title == product_name)
            )
            product = result.scalar_one_or_none()
            if not product:
                raise HTTPException(
                    status_code=404, detail="Product not found"
                )
            await session.delete(product)
            await session.commit()
            return {"message": "Product deleted"}
