import os
import io, zipfile
from typing import Annotated
from fastapi import APIRouter, UploadFile as UF, File, status
from fastapi.params import Depends
from pydantic import WithJsonSchema
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse, FileResponse

from core.db_connect import get_session
from src.services.image_service import image_service

router = APIRouter(prefix="/api/v1/images/product", tags=["files"])

UploadFile = Annotated[
    UF, WithJsonSchema({"type": "string", "format": "binary"})
]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product_images(
    barcode: int,
    uploaded_files: list[UploadFile] = File(...),
    session: AsyncSession = Depends(get_session),
):
    images = await image_service.create_product_image(
        barcode, uploaded_files, session
    )
    return {"message": "success saved", "images count": images}


@router.get("/", status_code=status.HTTP_200_OK)
async def get_product_images(
    barcode: int, session: AsyncSession = Depends(get_session)
):
    images = await image_service.get_product_images(barcode, session)

    return FileResponse(images)
