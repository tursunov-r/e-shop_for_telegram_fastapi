import os
import uuid

from fastapi import UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.image_repository import image_repository


class ImageService:
    @staticmethod
    async def create_product_image(
        barcode: int, files: list[UploadFile], session: AsyncSession
    ):
        upload_dir = f"src/resources/images/products/{barcode}"
        os.makedirs(upload_dir, exist_ok=True)
        images = []

        for uploaded_file in files:
            contents = await uploaded_file.read()
            filename = f"{uuid.uuid4()}_{uploaded_file.filename}".replace(
                " ", "_"
            )
            path = f"{upload_dir}/{filename}"
            print(path)
            filepath = os.path.join(upload_dir, filename)
            images.append(filepath)
            with open(filepath, "wb") as f:
                f.write(contents)
        save_images = await image_repository.create_product_image(
            barcode=barcode, files=images, session=session
        )
        return save_images

    @staticmethod
    async def get_product_images(barcode: int, session: AsyncSession):
        def file_cut(files: str):
            with open(files, "rb") as f:
                while chunk := f.read(1024 * 1024):
                    yield chunk

        images = await image_repository.get_product_images(
            barcode=barcode, session=session
        )
        return images


image_service = ImageService()
