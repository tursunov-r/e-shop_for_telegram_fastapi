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
    async def create_order(
        new_order: CreateOrderSchema, session: AsyncSession
    ):
        order = await order_repo.create_order_query(
            user_id=new_order.user_id,
            products=new_order.product_ids,
            session=session,
        )
        if not order:
            raise
        return order

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

    @staticmethod
    async def get_user_orders(user_id: int, session: AsyncSession):
        orders = await order_repo.get_user_orders_query(
            user_id=user_id, session=session
        )
        return orders
