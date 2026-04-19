from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from src.models.order_model import OrderModel, OrderItemModel
from src.schemas.order_schema import ProductItem
from src.models.product_model import ProductModel
from src.models.user_model import UserModel
from src.services.product_service import product_repo


class OrderRepository:
    @staticmethod
    async def create_order_query(
        user_id: int, products: list[ProductItem], session: AsyncSession
    ):
        try:
            order = OrderModel(user_id=user_id, total=Decimal(0))
            session.add(order)
            total_sum = Decimal(0)
            for item in products:
                await product_repo.update_product_quantity(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    session=session,
                )
                result = await session.execute(
                    select(ProductModel).where(
                        ProductModel.id == item.product_id
                    )
                )
                product = result.scalar_one_or_none()
                if not product:
                    raise ValueError(f"Product {item.product_id} not found")

                item_total = product.price * item.quantity
                total_sum += item_total

                order_item = OrderItemModel(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=item.quantity,
                    total=item_total,
                )
                session.add(order_item)

            order.total = total_sum
            return order
        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_all_orders_query(session: AsyncSession):
        result = await session.execute(select(OrderModel))
        orders = result.scalars().all()
        return orders

    @staticmethod
    async def get_order_by_id_query(order_id: int, session: AsyncSession):
        result = await session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order:
            return order
        return None

    @staticmethod
    async def get_order_items_query(order_id: int, session: AsyncSession):
        result = await session.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        order_items = result.scalars().all()
        if order_items:
            return order_items
        raise ValueError(f"Order {order_id} not found")

    @staticmethod
    async def update_order_query(
        session: AsyncSession,
        order_id: int,
        status: str = None,
    ):
        result = await session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        order = result.scalar_one_or_none()
        if not order:
            return None
        if status is not None:
            order.status = status
        session.add(order)
        return order

    @staticmethod
    async def get_user_orders_query(user_id: int, session: AsyncSession):
        try:
            result = await session.execute(
                select(UserModel)
                .options(
                    joinedload(UserModel.orders)
                    .joinedload(OrderModel.items)
                    .joinedload(OrderItemModel.product)
                )
                .where(UserModel.id == user_id)
            )
            orders = result.unique().scalars().all()
            return orders
        except Exception as e:
            raise e

    @staticmethod
    async def update_order_status_query(
        order_id: int, status: str, session: AsyncSession
    ):
        result = await session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        order = result.scalar_one_or_none()
        if not order:
            raise ValueError(f"Order {order_id} not found")
        if order.status == status:
            raise ValueError(f"Order {order_id} already {status}")
        order.status = status
        session.add(order)
