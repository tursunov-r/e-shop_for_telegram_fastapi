import asyncio

from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload
from src.utils.exceptions.exceptions import NotFound

from models import ProductModel, ProductImageModel


class ImageRepository:
    @staticmethod
    async def _product_image(
        product_id: int, path: str, session: AsyncSession
    ):
        image = ProductImageModel(product_id=product_id, path_to_image=path)
        session.add(image)

    @staticmethod
    async def create_product_image(
        barcode: int, files: list[str], session: AsyncSession
    ):
        product_id = await session.execute(
            select(ProductModel.id).where(ProductModel.barcode == str(barcode))
        )
        product_id = product_id.scalar_one_or_none()
        for file in files:
            await ImageRepository._product_image(product_id, file, session)
        return len(files)

    @staticmethod
    async def get_product_images(barcode: int, session: AsyncSession):
        product_id = await session.execute(
            select(ProductModel.id).where(ProductModel.barcode == str(barcode))
        )
        product_id = product_id.scalar_one_or_none()
        images = await session.execute(
            select(ProductImageModel.path_to_image).where(
                ProductImageModel.product_id == product_id
            )
        )
        if not images:
            return None
        images = images.scalars().all()
        return images


image_repository = ImageRepository()
