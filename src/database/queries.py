from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connect import create_session, engine
from src.database.models import (
    Base,
    UserModel,
    OrderModel,
    ProductModel,
    OrderItemModel,
)
from src.schemas.schemas import (
    CreateProductSchema,
    UpdateProductSchema,
    ProductItem,
)


async def create_tables():
    async with engine.begin() as conn:
        engine.echo = False
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"message": "Tables created."}


async def create_products_query(
    product: CreateProductSchema,
):
    async with create_session() as session:
        try:
            product = ProductModel(
                title=product.title,
                quantity=product.quantity,
                price=Decimal(product.price),
                description=product.description,
            )
            session.add(product)
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise e


async def update_product_in_db_query(product_id, data):
    async with create_session() as session:
        try:
            result = await session.execute(
                select(ProductModel).where(ProductModel.id == product_id)
            )
            product = result.scalar_one_or_none()
            if not product:
                raise ValueError(f"Product {product_id} not found")

            product.title = data["title"]
            product.quantity = data["quantity"]
            product.price = data["price"]
            product.description = data["description"]

            await session.commit()
            await session.refresh(product)
            return product
        except Exception as e:
            await session.rollback()
            raise e


async def create_user_query(name: str, email: str, balance: Decimal = None):
    async with create_session() as session:
        try:
            user = UserModel(name=name, email=email, balance=balance)
            session.add(user)
            await session.commit()
            return user
        except Exception as e:
            await session.rollback()
            raise e


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
            await session.commit()
            await session.refresh(order)
            return order
        except Exception as e:
            await session.rollback()
            raise e


async def get_all_orders_query():
    async with create_session() as session:
        result = await session.execute(select(OrderModel))
        orders = result.scalars().all()
        return orders


async def get_order_by_id_query(order_id):
    async with create_session() as session:
        result = await session.execute(
            select(OrderModel).where(OrderModel.id == order_id)
        )
        order = result.scalar_one_or_none()
        if order:
            return order
        return None


async def get_order_items_query(order_id):
    async with create_session() as session:
        result = await session.execute(
            select(OrderItemModel).where(OrderItemModel.order_id == order_id)
        )
        order_items = result.scalars().all()
        if order_items:
            return order_items
        return None


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


async def get_all_products_from_db_query():
    async with create_session() as session:
        result = await session.execute(select(ProductModel))
        products = result.scalars().all()
        return [
            {
                "id": product.id,
                "title": product.title,
                "quantity": product.quantity,
                "price": float(product.price),
            }
            for product in products
        ]


async def get_product_by_id_from_db_query(product_id: int):
    async with create_session() as session:
        result = await session.execute(
            select(ProductModel).where(ProductModel.id == product_id)
        )
        product = result.scalar_one_or_none()
        return product


async def update_product_query(product_name: str, update: UpdateProductSchema):
    async with create_session() as session:
        result = await session.execute(
            select(ProductModel).where(ProductModel.title == product_name)
        )
        product = result.scalar_one_or_none()
        if not product:
            raise ValueError(f"Product {product_name} not found")

        # Обновляем только непустые поля
        if update.title is not None:
            product.title = update.title
        if update.quantity is not None:
            product.quantity = update.quantity
        if update.price is not None:
            product.price = Decimal(update.price)
        if update.description is not None:
            product.description = update.description

        await session.commit()
        await session.refresh(product)
        return product


async def delete_product_query(product_name: str):
    async with create_session() as session:
        result = await session.execute(
            select(ProductModel).where(ProductModel.title == product_name)
        )
        product = result.scalar_one_or_none()
        if not product:
            return None
        await session.delete(product)
        await session.commit()
        return {"message": "Product deleted"}


async def get_user_orders_query(user_id: int):
    async with create_session() as session:
        result = await session.execute(
            select(UserModel)
            .options(
                joinedload(UserModel.orders).joinedload(OrderModel.products)
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
