from decimal import Decimal
from typing import Optional, List, Dict

from fastapi import APIRouter, status, Request, Response
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.core.db_connect import get_session
from src.services.product_service import ProductService

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
    GetProductSchema,
)
from src.core.limiter import limiter

router_v1 = APIRouter(prefix="/api/v1/products", tags=["products v1"])

product_service = ProductService()


@router_v1.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
@limiter.limit("30/minute")
async def create_product(
    product: CreateProductSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    create = await product_service.create_product(
        product=product, session=session
    )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"message": "created"}
    )


@router_v1.get("/title/{product_title}", response_model=List[GetProductSchema])
@limiter.limit("30/minute")
async def search_product(
    product_title: str,
    request: Request,
    product_min_price: Optional[Decimal] = None,
    product_max_price: Optional[Decimal] = None,
    session: AsyncSession = Depends(get_session),
):
    product = await product_service.search_products(
        title=product_title,
        min_price=product_min_price,
        max_price=product_max_price,
        session=session,
    )
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
    product = await product_service.get_product_by_id(
        product_id=product_id, session=session
    )
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
    products = await product_service.get_products(session=session)
    return products


@router_v1.delete("/{product_title}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1/hour")
async def delete_product(
    product_title: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    await product_service.delete_product(
        product_title=product_title,
        session=session,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router_v1.patch(
    "/{product_name}",
    status_code=status.HTTP_200_OK,
    response_model=GetProductSchema,
)
@limiter.limit("30/minute")
async def update_product(
    product_name: str,
    product: UpdateProductSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    update = await product_service.update_product(
        product_name=product_name,
        product=product,
        session=session,
    )
    return update
