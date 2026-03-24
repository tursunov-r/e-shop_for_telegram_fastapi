from random import choice
from decimal import Decimal

from src.database.queries import (
    create_products,
    create_user,
    create_order,
)
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


async def create_data():
    for product in products:
        schema = CreateProductSchema(**product)
        await create_products(schema)
    await create_user(
        name="Alice", email="alice@examle.com", balance=Decimal(10000.00)
    )
    await create_user(name="Bob", email="bob@example.com")

    # Для имитации заказа, рандомный выбор между двумя пользователями
    user_ids = [1, 2]
    # Рандомный выбор между двумя товарами
    product_ids = [1, 2]

    for order in range(1, 101):
        await create_order(
            user_id=choice(user_ids), products=[(choice(product_ids), 1)]
        )
