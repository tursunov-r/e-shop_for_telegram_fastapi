from fastapi import APIRouter, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.order_service import OrderService
from src.schemas.order_schema import (
    CreateOrderSchema,
    UpdateOrderSchema,
)
from src.core.db_connect import get_session

from src.services.log_service import log_service

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
    log_service.info(
        "order created successfully: ",
        order_id=result[0].id,
        email=result[1],
    )
    return result


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int, session: AsyncSession = Depends(get_session)
):
    result = await service.get_order_by_id(order_id=order_id, session=session)
    log_service.info("order retrieved successfully: ", order_id=order_id)
    return result


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    orders = await service.get_user_orders(user_id=user_id, session=session)
    log_service.info("order retrieved successfully: ", orders=user_id)
    return orders


@router.patch("/{order_id}")
async def update_order(
    order: UpdateOrderSchema, session: AsyncSession = Depends(get_session)
):
    result = await service.update_order(order=order, session=session)
    log_service.info("order updated successfully: ", order=order)
    return result


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(session: AsyncSession = Depends(get_session)):
    result = await service.get_orders(session=session)
    log_service.info("order get successfully: ", result=result[0])
    return result
