from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.core.db_connect import create_session
from src.models.order_model import OrderModel, OrderItemModel
from src.schemas.order_schema import ProductItem
from src.models.product_model import ProductModel
from src.models.user_model import UserModel


class OrderRepository:
    @staticmethod
    async def create_order_query(user_id: int, products: list[ProductItem]):
        async with create_session() as session:
            try:
                order = OrderModel(user_id=user_id, total=Decimal(0))
                session.add(order)
                await session.flush()

                total_sum = Decimal(0)
                for item in products:
                    result = await session.execute(
                        select(ProductModel).where(
                            ProductModel.id == item.product_id
                        )
                    )
                    product = result.scalar_one_or_none()
                    if not product:
                        raise ValueError(
                            f"Product {item.product_id} not found"
                        )

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
                await session.commit()
                await session.refresh(order)
                return order
            except Exception as e:
                await session.rollback()
                raise e

    @staticmethod
    async def get_all_orders_query():
        async with create_session() as session:
            result = await session.execute(select(OrderModel))
            orders = result.scalars().all()
            return orders

    @staticmethod
    async def get_order_by_id_query(order_id):
        async with create_session() as session:
            result = await session.execute(
                select(OrderModel).where(OrderModel.id == order_id)
            )
            order = result.scalar_one_or_none()
            if order:
                return order
            return None

    @staticmethod
    async def get_order_items_query(order_id):
        async with create_session() as session:
            result = await session.execute(
                select(OrderItemModel).where(
                    OrderItemModel.order_id == order_id
                )
            )
            order_items = result.scalars().all()
            if order_items:
                return order_items
            return None

    @staticmethod
    async def update_order_query(order_id: int, status: str = None):
        async with create_session() as session:
            result = await session.execute(
                select(OrderModel).where(OrderModel.id == order_id)
            )
            order = result.scalar_one_or_none()
            if not order:
                return None
            if status is not None:
                order.status = status
            session.add(order)
            await session.commit()
            await session.refresh(order)
            return order

    @staticmethod
    async def get_user_orders_query(user_id: int):
        async with create_session() as session:
            result = await session.execute(
                select(UserModel)
                .options(
                    joinedload(UserModel.orders).joinedload(
                        OrderModel.products
                    )
                )
                .where(UserModel.id == user_id)
            )
            user = result.unique().scalar_one_or_none()

            if not user:
                return None

            orders_data = []
            for order in user.orders:
                products = [
                    {
                        "id": product.id,
                        "title": product.title,
                        "price": float(product.price),
                    }
                    for product in order.products
                ]
                orders_data.append(
                    {
                        "order_id": order.id,
                        "total": float(order.total),
                        "created_at": order.created_at,
                        "products": products,
                    }
                )
            return orders_data

    @staticmethod
    async def update_order_status_query(order_id: int, status: str):
        async with create_session() as session:
            result = await session.execute(
                select(OrderModel).where(OrderModel.id == order_id)
            )
            order = result.scalar_one_or_none()
            if not order:
                raise ValueError(f"Order {order_id} not found")
            if order.status == status:
                raise ValueError(f"Order {order_id} already {status}")
            order.status = status
            await session.commit()
