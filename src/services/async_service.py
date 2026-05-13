import asyncio
import time
from random import choice

from fastapi import Depends

from src.core.db_connect import get_session
from src.repositories.order_repository import OrderRepository

statuses = ["created", "rady to ship", "delivery", "processed"]


async def process_order_async(order_id: int, status: str) -> dict:
    try:
        order_repo = OrderRepository()
        await asyncio.sleep(0.1)  # имитация запроса
        await order_repo.update_order_status_query(
            order_id=order_id, status=status, session=Depends(get_session)
        )
        return {"message": f"Order {order_id} status is {status}."}
    except Exception as e:
        return {"message": f"Something went wrong. {str(e)}"}


async def process_orders_async(orders: list):
    tasks = [
        process_order_async(order_id=order, status=choice(statuses))
        for order in orders
    ]
    results = await asyncio.gather(*tasks)
    return results
