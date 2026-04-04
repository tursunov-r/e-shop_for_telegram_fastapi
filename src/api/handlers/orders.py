from fastapi import APIRouter, status, HTTPException

from src.database.queries import (
    create_order_query,
    get_all_orders_query,
    get_order_by_id_query,
    get_order_items_query,
    update_order_query,
)
from src.schemas.schemas import CreateOrderSchema, UpdateOrderSchema

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderSchema):
    """Функция создает заказ
    -id пользователя
    -id товара передаются кортежем (id товара, количество)
    """
    try:
        order_id = await create_order_query(
            user_id=order.user_id, products=order.product_ids
        )
        return {
            "message": "success",
            "data": order_id,
            "status": status.HTTP_201_CREATED,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong",
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders():
    orders = await get_all_orders_query()
    return orders


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int):
    order = await get_order_by_id_query(order_id)
    items = await get_order_items_query(order_id)
    if not order or not items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
    return {"order details": order, "order items": items}


@router.patch("/{order_id}")
async def update_order(order: UpdateOrderSchema):
    result = await update_order_query(
        order_id=order.order_id, status=order.status
    )
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order.order_id} not found",
        )
    return result
