import os
import uuid
import json
from decimal import Decimal
from typing import Optional, List, Annotated

from fastapi import (
    APIRouter,
    status,
    Request,
    Response,
    UploadFile as UF,
    File,
    Form,
)
from fastapi.params import Depends
from pydantic import WithJsonSchema
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_connect import get_session
from src.schemas.user_schemas import TokenData
from src.services.log_service import log_service
from src.services.product_service import product_service

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
    GetProductSchema,
)
from src.core.limiter import limiter
from src.utils.auth import get_current_user

router_v1 = APIRouter(prefix="/api/v1/products", tags=["products v1"])

UploadFile = Annotated[
    UF, WithJsonSchema({"type": "string", "format": "binary"})
]


@router_v1.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_product(
    request: Request,
    product: CreateProductSchema,
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(get_current_user),
):
    """
    Create a new product
    """

    create = await product_service.create_product(
        product=product, session=session, user=user
    )
    log_service.info("created product", create=create)
    return {"message": "create", "product": create}


@router_v1.get("/search/{search}", response_model=List[GetProductSchema])
@limiter.limit("30/minute")
async def search_product(
    search: str,
    request: Request,
    product_min_price: Optional[Decimal] = None,
    product_max_price: Optional[Decimal] = None,
    session: AsyncSession = Depends(get_session),
):
    """
    Search product with title or barcode
    """
    product = await product_service.search_products(
        search=search,
        min_price=product_min_price,
        max_price=product_max_price,
        session=session,
    )
    log_service.info("searching product", product=product)
    return product


@router_v1.get(
    "/id/{product_id}",
    status_code=status.HTTP_200_OK,
    response_model=GetProductSchema,
)
@limiter.limit("30/minute")
async def get_product_by_id(
    product_id: int,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    """
    Get product by id
    """
    product = await product_service.get_product_by_id(
        product_id=product_id, session=session
    )
    log_service.info("getting product", product=product)
    return product


@router_v1.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[GetProductSchema],
)
@limiter.limit("30/minute")
async def get_products(
    request: Request, session: AsyncSession = Depends(get_session)
):
    """
    get all products
    """
    products = await product_service.get_products(session=session)
    log_service.info("getting products", products=products)
    return products


@router_v1.delete("/barcode/{barcode}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("100/hour")
async def delete_product(
    barcode: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(get_current_user),
):
    """
    Delete product by barcode
    """
    await product_service.delete_product(
        barcode=barcode,
        session=session,
        user=user,
    )
    log_service.info("deleted product", product=barcode)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_v1.delete("/id/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/hour")
async def delete_product_id(
    request: Request,
    product_id: int,
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(get_current_user),
):
    """
    Delete product by id
    """
    result = await product_service.delete_product_by_id(
        product_id=product_id, session=session, user=user
    )
    log_service.info("deleted product", product=product_id)
    return result


@router_v1.patch(
    "/{barcode}",
    status_code=status.HTTP_200_OK,
    response_model=GetProductSchema,
)
@limiter.limit("30/minute")
async def update_product(
    barcode: str,
    product: UpdateProductSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(get_current_user),
):
    """
    Update product, for finding product take barcode
    """
    update = await product_service.update_product(
        barcode=barcode,
        product=product,
        session=session,
        user=user,
    )
    log_service.info("updated product", update=update)
    return update
