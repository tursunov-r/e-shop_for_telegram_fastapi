import asyncio
import time
from random import choice

from order_service.src.database.query import update_order_status_query

statuses = ["created", "rady to ship", "delivery", "processed"]


async def process_order_async(order_id: int, status: str) -> dict:
    try:
        await asyncio.sleep(0.1)  # имитация запроса
        await update_order_status_query(order_id, status)
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


async def main():
    orders_list: list = list(range(1, 101))
    start_time = time.time()
    result = await process_orders_async(orders=orders_list)
    end_time = time.time()
    print("Async process time:", end_time - start_time)
    print("Result:", result)
    return result


if __name__ == "__main__":
    asyncio.run(main())
