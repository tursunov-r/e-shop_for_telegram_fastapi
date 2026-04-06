from fastapi import APIRouter, status, HTTPException

from order_service.src.services.order import OrderService
from order_service.src.schemas.schemas import (
    CreateOrderSchema,
    UpdateOrderSchema,
)

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
service = OrderService()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(order: CreateOrderSchema):
    """Функция создает заказ
    -id пользователя
    -id товара передаются кортежем (id товара, количество)
    """
    try:
        result = await service.create_order(order)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong",
        )


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(order_id: int):
    try:
        result = await service.get_order_by_id(order_id)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )


@router.patch("/{order_id}")
async def update_order(order: UpdateOrderSchema):
    try:
        result = await service.update_order(order)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong",
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders():
    try:
        result = await service.get_orders()
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not orders yet"
        )
