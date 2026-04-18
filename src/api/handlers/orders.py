from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.order_service import OrderService
from src.schemas.order_schema import (
    CreateOrderSchema,
    UpdateOrderSchema,
)
from src.core.db_connect import get_session

router = APIRouter(prefix="/api/v1/orders", tags=["orders"])
service = OrderService()


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_order(
    order: CreateOrderSchema, session: AsyncSession = Depends(get_session)
):
    """Функция создает заказ
    -id пользователя
    -id товара передаются кортежем (id товара, количество)
    """
    result = await service.create_order(new_order=order, session=session)
    return result


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        result = await service.get_order_by_id(
            order_id=order_id, session=session
        )
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    orders = await service.get_user_orders(user_id=user_id, session=session)
    return orders


@router.patch("/{order_id}")
async def update_order(
    order: UpdateOrderSchema, session: AsyncSession = Depends(get_session)
):
    try:
        result = await service.update_order(order=order, session=session)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Something went wrong",
        )


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(session: AsyncSession = Depends(get_session)):
    try:
        result = await service.get_orders(session=session)
        return result
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Not orders yet"
        )
