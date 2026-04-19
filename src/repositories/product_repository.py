from decimal import Decimal

from sqlalchemy import select
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.product_model import ProductModel
from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)


class ProductRepository:
    @staticmethod
    async def create_products_query(
        product: CreateProductSchema,
        session: AsyncSession,
    ):
        if len(product.title.strip()) == 0:
            raise HTTPException(
                status_code=400, detail="Product name cannot be empty"
            )
        new_product = ProductModel(
            title=product.title.title().strip(),
            quantity=product.quantity,
            price=Decimal(product.price),
            description=product.description,
        )
        session.add(new_product)
        return new_product

    @staticmethod
    async def get_all_products_from_db_query(session: AsyncSession):
        result = await session.execute(select(ProductModel))
        products = result.scalars().all()
        if products:
            return [item for item in products]
        raise HTTPException(status_code=404, detail="No products yet")

    @staticmethod
    async def get_product_by_id_from_db_query(
        product_id: int, session: AsyncSession
    ):
        result = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = result.scalar_one_or_none()
        if product:
            return product
        raise HTTPException(status_code=404, detail="Product not found")

    @staticmethod
    async def search_product(
        title: str,
        min_price: Decimal,
        max_price: Decimal,
        session: AsyncSession,
    ):
        if not min_price:
            min_price = await session.execute(
                select(ProductModel.price)
                .order_by(ProductModel.price)
                .limit(1)
            )
            min_price = min_price.scalar_one_or_none()
        if not max_price:
            max_price = await session.execute(
                select(ProductModel.price)
                .order_by(ProductModel.price.desc())
                .limit(1)
            )
            max_price = max_price.scalar_one_or_none()
        print(title, min_price, max_price)
        result = await session.execute(
            select(ProductModel)
            .where(ProductModel.title.ilike(f"%{title}%"))
            .where(ProductModel.price.between(min_price, max_price))
        )
        products = result.scalars().all()
        if products:
            return [item for item in products]
        raise HTTPException(status_code=404, detail="No products yet")

    @staticmethod
    async def update_product_query(
        product_name: str,
        update: UpdateProductSchema,
        session: AsyncSession,
    ):
        result = await session.execute(
            select(ProductModel).where(
                ProductModel.title == product_name.title().strip()
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        # Обновляем только непустые поля
        if update.title is not None:
            product.title = update.title
        if update.quantity is not None:
            product.quantity = update.quantity
        if update.price is not None:
            product.price = Decimal(update.price)
        if update.description is not None:
            product.description = update.description

        return product

    @staticmethod
    async def update_product_quantity(
        product_id: int, quantity: int, session: AsyncSession
    ):
        product = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = product.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        if product.quantity < quantity:
            raise HTTPException(status_code=404, detail="Not enough products")
        product.quantity -= quantity
        return product

    @staticmethod
    async def delete_product_query(product_name: str, session: AsyncSession):
        result = await session.execute(
            select(ProductModel).where(
                ProductModel.title == product_name.title().strip()
            )
        )
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        await session.delete(product)
        return {"message": "Product deleted"}
