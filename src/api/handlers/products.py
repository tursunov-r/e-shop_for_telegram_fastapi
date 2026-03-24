from fastapi import APIRouter, HTTPException, Response

from src.database.queries import (
    get_all_products_from_db,
    get_product_by_id_from_db,
    create_products,
)
from src.schemas.schemas import ProductSchema

router = APIRouter(prefix="/api/v1/products", tags=["products"])


@router.post("/create")
async def create_product(product: ProductSchema):
    try:
        if product.price < 0:
            raise HTTPException(
                status_code=400, detail="Price cannot be negative"
            )
        if product.quantity < 0:
            raise HTTPException(
                status_code=400, detail="Quantity cannot be negative"
            )
        await create_products(
            title=product.title,
            description=product.description,
            price=product.price,
            quantity=product.quantity,
        )
    except HTTPException as e:
        raise HTTPException(
            status_code=400, detail=f"Something went wrong: {e}"
        )


@router.get("/{id}")
async def get_product_by_id(product_id: int):
    product = await get_product_by_id_from_db(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.get("/")
async def get_products():
    products = get_all_products_from_db()
    return {"products": products}
