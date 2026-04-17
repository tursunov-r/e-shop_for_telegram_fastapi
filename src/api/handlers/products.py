from decimal import Decimal
from typing import Optional

from fastapi import APIRouter, status, Request

from src.services.product_service import ProductService

from src.schemas.product_schemas import (
    CreateProductSchema,
    UpdateProductSchema,
)
from src.core.limiter import limiter

router_v1 = APIRouter(prefix="/api/v1/products", tags=["products v1"])

product_service = ProductService()


@router_v1.post("/", status_code=status.HTTP_201_CREATED)
@limiter.limit("30/minute")
async def create_product(
    product: CreateProductSchema,
    request: Request,
):
    create = await product_service.create_product(product=product)
    return create


@router_v1.get("/{product_title}")
@limiter.limit("30/minute")
async def search_product(
    product_title: str,
    request: Request,
    product_min_price: Optional[Decimal] = None,
    product_max_price: Optional[Decimal] = None,
):
    product_title = await product_service.search_products(
        title=product_title,
        min_price=product_min_price,
        max_price=product_max_price,
    )
    return product_title


@router_v1.get("/{product_id}", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def get_product_by_id(product_id: int, request: Request):
    product = await product_service.get_product_by_id(product_id)
    return product


@router_v1.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def get_products(request: Request):
    products = await product_service.get_products()
    return products


@router_v1.delete("/{product_title}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("1/hour")
async def delete_product(
    product_title: str,
    authorization: str,
    request: Request,
):
    deleted = await product_service.delete_product(
        product_title, authorization
    )
    return deleted


@router_v1.patch("/{product_name}", status_code=status.HTTP_200_OK)
@limiter.limit("30/minute")
async def update_product(
    product_name: str,
    product: UpdateProductSchema,
    authorization: str,
    request: Request,
):
    update = await product_service.update_product(
        product_name=product_name, product=product, authorization=authorization
    )
    return update
