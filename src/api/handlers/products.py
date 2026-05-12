from decimal import Decimal
from typing import Optional, List

from fastapi import APIRouter, status, Request, Response, HTTPException
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from src.core.db_connect import get_session
from src.services.log_service import log_service
from src.services.product_service import ProductService

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
    GetProductSchema,
)
from src.core.limiter import limiter
from src.utils.statuses import get_status_code

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
    try:
        create = await product_service.create_product(
            product=product, session=session
        )
        log_service.info("created product", create=create)
        return Response(
            status_code=status.HTTP_201_CREATED, content={"message": "created"}
        )
    except Exception as e:
        log_service.error(
            "error creating product", code=get_status_code(e), exception=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router_v1.get("/title/{product_title}", response_model=List[GetProductSchema])
@limiter.limit("30/minute")
async def search_product(
    product_title: str,
    request: Request,
    product_min_price: Optional[Decimal] = None,
    product_max_price: Optional[Decimal] = None,
    session: AsyncSession = Depends(get_session),
):
    try:
        product = await product_service.search_products(
            title=product_title,
            min_price=product_min_price,
            max_price=product_max_price,
            session=session,
        )
        log_service.success("searching product", product=product)
        return product
    except Exception as e:
        log_service.error(
            "error searching product", code=get_status_code(e), error=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


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
    try:
        product = await product_service.get_product_by_id(
            product_id=product_id, session=session
        )
        log_service.success("getting product", product=product)
        return product
    except Exception as e:
        log_service.error(
            "product not found",
            product_id=product_id,
            code=get_status_code(e),
            error=str(e),
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router_v1.get(
    "/",
    status_code=status.HTTP_200_OK,
    response_model=List[GetProductSchema],
)
@limiter.limit("30/minute")
async def get_products(
    request: Request, session: AsyncSession = Depends(get_session)
):
    try:
        products = await product_service.get_products(session=session)
        log_service.info("getting products", products=products)
        return products
    except Exception as e:
        log_service.error(
            "error getting products", code=get_status_code(e), error=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router_v1.delete(
    "/title/{product_title}", status_code=status.HTTP_204_NO_CONTENT
)
@limiter.limit("1/hour")
async def delete_product(
    product_title: str,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    try:
        await product_service.delete_product(
            product_title=product_title,
            session=session,
        )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        log_service.error(
            "error deleting product", code=get_status_code(e), error=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router_v1.delete("/id/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("10/hour")
async def delete_product_id(
    request: Request,
    product_id: int,
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await product_service.delete_product_by_id(
            product_id=product_id, session=session
        )
        return result
    except Exception as e:
        log_service.error(
            "error deleting product",
            product=product_id,
            code=get_status_code(e),
            error=str(e),
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


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
    try:
        update = await product_service.update_product(
            product_name=product_name,
            product=product,
            session=session,
        )
        log_service.success("updated product", update=update)
        return update
    except Exception as e:
        log_service.error(
            "error updating product", code=get_status_code(e), error=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))
