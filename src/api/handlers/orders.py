from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.order_service import OrderService
from src.schemas.order_schema import (
    CreateOrderSchema,
    UpdateOrderSchema,
)
from src.core.db_connect import get_session

from src.services.log_service import log_service
from src.utils.statuses import get_status_code

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
    try:
        result = await service.create_order(new_order=order, session=session)
        log_service.info(
            "order created successfully: ",
            order_id=result[0].id,
            email=result[1],
        )
        return result
    except Exception as e:
        log_service.error(
            "error creating order",
            user=order.user_id,
            code=get_status_code(e),
            exception=str(e),
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.get("/{order_id}", status_code=status.HTTP_200_OK)
async def get_order(
    order_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        result = await service.get_order_by_id(
            order_id=order_id, session=session
        )
        log_service.info("order retrieved successfully: ", order_id=order_id)
        return result
    except Exception as e:
        log_service.error(
            "error retrieving order",
            order=order_id,
            code=get_status_code(e),
            exception=str(e),
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.get("/user/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_orders(
    user_id: int, session: AsyncSession = Depends(get_session)
):
    try:
        orders = await service.get_user_orders(
            user_id=user_id, session=session
        )
        log_service.info("order retrieved successfully: ", orders=user_id)
        return orders
    except Exception as e:
        log_service.error(
            "error retrieving user orders",
            user=user_id,
            code=get_status_code(e),
            exception=str(e),
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.patch("/{order_id}")
async def update_order(
    order: UpdateOrderSchema, session: AsyncSession = Depends(get_session)
):
    try:
        result = await service.update_order(order=order, session=session)
        log_service.info("order updated successfully: ", order=order)
        return result
    except Exception as e:
        log_service.error(
            "error updating order",
            order=order,
            code=get_status_code(e),
            exception=str(e),
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.get("/", status_code=status.HTTP_200_OK)
async def get_orders(session: AsyncSession = Depends(get_session)):
    try:
        result = await service.get_orders(session=session)
        log_service.info("order get successfully: ", result=result[0])
        return result
    except Exception as e:
        log_service.error(
            "error get order", code=get_status_code(e), exception=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))
