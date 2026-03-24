from random import choice
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from src.database.connect import get_session, engine
from src.database.models import (
    Base,
    UserModel,
    OrderModel,
    ProductModel,
    OrderItemModel,
)


def create_tables():
    engine.echo = False
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


create_tables()


def create_products(
    title: str, quantity: int, price: Decimal, description: str
):
    with get_session() as session:
        try:
            product = ProductModel(
                title=title,
                quantity=quantity,
                price=price,
                description=description,
            )
            session.add(product)
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


def update_product_in_db(product_id, data):
    with get_session() as session:
        try:
            product = session.query(ProductModel).get(product_id)
            product.title = data["title"]
            product.quantity = data["quantity"]
            product.price = data["price"]
            product.description = data["description"]
            session.add_all(
                [
                    product.title,
                    product.quantity,
                    product.price,
                    product.description,
                ]
            )
            session.commit()
        except Exception as e:
            session.rollback()
            raise e


def create_user(name: str, email: str, balance: Decimal = None):
    with get_session() as session:
        try:
            user = UserModel(name=name, email=email, balance=balance)
            session.add(user)
            session.commit()
            return user
        except Exception as e:
            session.rollback()
            raise e


def create_order(user_id: int, products: list[tuple[int, int]]):
    with get_session() as session:
        try:
            order = OrderModel(user_id=user_id, total=Decimal(0))
            session.add(order)
            session.flush()  # получить номер заказа

            total_sum = Decimal(0)
            for products_id, quantity in products:
                product = session.get(ProductModel, products_id)
                if not product:
                    raise ValueError(f"Product {products_id} not found")
                item_total = product.price * quantity
                total_sum += item_total
                order_item = OrderItemModel(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=quantity,
                    total=item_total,
                )
                session.add(order_item)

            order.total = total_sum
            session.commit()
            session.refresh(order)
            return order
        except Exception as e:
            session.rollback()
            raise e


def get_all_products_from_db():
    with get_session() as session:
        products = session.query(ProductModel).all()
        return [
            {
                "id": product.id,
                "title": product.title,
                "quantity": product.quantity,
                "price": float(product.price),
            }
            for product in products
        ]


def get_product_by_id_from_db(product_id: int):
    with get_session() as session:
        try:
            product = (
                session.query(ProductModel)
                .where(ProductModel.id == product_id)
                .first()
            )
            if not product:
                raise ValueError(f"Product {product_id} not found")
            return {
                "id": product.id,
                "title": product.title,
                "quantity": product.quantity,
                "price": float(product.price),
                "description": product.description,
            }
        except Exception as e:
            raise e


def get_user_orders(user_id: int):
    with get_session() as session:
        user = (
            session.query(UserModel)
            .options(
                joinedload(UserModel.orders).joinedload(OrderModel.products)
            )
            .filter(UserModel.id == user_id)
            .first()
        )

        if not user:
            return None

        result = []
        for order in user.orders:
            products = [
                {
                    "id": product.id,
                    "title": product.title,
                    "price": product.price,
                }
                for product in order.products
            ]
            result.append(
                {
                    "order_id": order.id,
                    "total": order.total,
                    "created_at": order.created_at,
                    "products": products,
                }
            )
        return result


def update_order_status(order_id: int, status: str):
    with get_session() as session:
        order = (
            session.query(OrderModel).filter(OrderModel.id == order_id).first()
        )
        if not order:
            raise ValueError(f"Order {order_id} not found")
        if order.status == status:
            raise ValueError(f"Order {order_id} already {status}")
        order.status = status
        session.commit()


create_products(
    title="MacBook air m3", quantity=10, price=Decimal(1000), description="M3"
)
create_products(
    title="iMac M4", quantity=10, price=Decimal(1900), description="M4"
)
create_user(name="Alice", email="alice@examle.com", balance=Decimal(10000.00))
create_user(name="Bob", email="bob@example.com")

# Для имитации заказа, рандомный выбор между двумя пользователями
user_ids = [1, 2]
# Рандомный выбор между двумя товарами
product_ids = [1, 2]


for order in range(1, 101):
    create_order(user_id=choice(user_ids), products=[(choice(product_ids), 1)])


print(get_user_orders(user_id=1))
print(get_user_orders(user_id=2))
print(get_all_products_from_db())
print(get_product_by_id_from_db(product_id=1))
