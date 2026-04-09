import random
from random import choice
from decimal import Decimal

from src.database.queries import (
    create_products_query,
    create_user_query,
)
from order_service.src.database.query import create_order_query
from order_service.src.schemas.schemas import ProductItem
from src.schemas.schemas import CreateProductSchema

products = [
    {
        "title": "MacBook air m3",
        "quantity": 10,
        "price": Decimal(1000),
        "description": "M3",
    },
    {
        "title": "iMac M4",
        "quantity": 10,
        "price": Decimal(1900),
        "description": "M4",
    },
]


# async def create_data():
#     for product in products:
#         schema = CreateProductSchema(**product)
#         await create_products_query(schema)
#     await create_user_query(
#         name="Alice", email="alice@examle.com", balance=Decimal(10000.00)
#     )
#     await create_user_query(name="Bob", email="bob@example.com")
#
#     # Для имитации заказа, рандомный выбор между двумя пользователями
#     user_ids = [1, 2]
#     # Рандомный выбор между двумя товарами
#     product_ids = [1, 2]
#
#     for order in range(1, 101):
#         await create_order_query(
#             user_id=choice(user_ids),
#             products=[
#                 ProductItem(
#                     product_id=(choice(product_ids)),
#                     quantity=random.randint(1, 10),
#                 )
#             ],
#         )
