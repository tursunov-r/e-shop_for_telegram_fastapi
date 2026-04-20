from fastapi import status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.order_schema import (
    CreateOrderSchema,
    UpdateOrderSchema,
)

from src.repositories.order_repository import OrderRepository


class OrderService:
    def __init__(self, order_repo: OrderRepository = OrderRepository()):
        self.order_repo = order_repo

    async def create_order(
        self, new_order: CreateOrderSchema, session: AsyncSession
    ):
        order = await self.order_repo.create_order_query(
            user_id=new_order.user_id,
            products=new_order.product_ids,
            session=session,
        )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
            )
        return order

    async def get_order_by_id(self, order_id: int, session: AsyncSession):
        order = await self.order_repo.get_order_by_id_query(
            order_id=order_id, session=session
        )
        items = await self.order_repo.get_order_items_query(
            order_id=order_id, session=session
        )
        if not order or not items:
            raise
        return {"order details": order, "order items": items}

    async def update_order(
        self, order: UpdateOrderSchema, session: AsyncSession
    ):
        result = await self.order_repo.update_order_query(
            order_id=order.order_id, status=order.status, session=session
        )
        if not result:
            raise
        return result

    async def get_orders(self, session: AsyncSession):
        orders = await self.order_repo.get_all_orders_query(session=session)
        return orders

    async def get_user_orders(self, user_id: int, session: AsyncSession):
        orders = await self.order_repo.get_user_orders_query(
            user_id=user_id, session=session
        )
        return orders
