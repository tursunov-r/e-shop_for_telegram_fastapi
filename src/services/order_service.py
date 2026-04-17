from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.order_schema import (
    CreateOrderSchema,
    UpdateOrderSchema,
)

from src.repositories.order_repository import OrderRepository

order_repo = OrderRepository()


class OrderService:
    @staticmethod
    async def create_order(order: CreateOrderSchema, session: AsyncSession):
        order_id = await order_repo.create_order_query(
            user_id=order.user_id, products=order.product_ids, session=session
        )
        if not order_id:
            raise
        return {
            "message": "success",
            "data": order_id,
            "status": status.HTTP_201_CREATED,
        }

    @staticmethod
    async def get_order_by_id(order_id: int, session: AsyncSession):
        order = await order_repo.get_order_by_id_query(
            order_id=order_id, session=session
        )
        items = await order_repo.get_order_items_query(
            order_id=order_id, session=session
        )
        if not order or not items:
            raise
        return {"order details": order, "order items": items}

    @staticmethod
    async def update_order(order: UpdateOrderSchema, session: AsyncSession):
        result = await order_repo.update_order_query(
            order_id=order.order_id, status=order.status, session=session
        )
        if not result:
            raise
        return result

    @staticmethod
    async def get_orders(session: AsyncSession):
        orders = await order_repo.get_all_orders_query(session=session)
        return orders
