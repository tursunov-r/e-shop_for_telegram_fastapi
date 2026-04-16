import asyncio


async def validate_order(order_id: int) -> dict:
    """Валидация заказа"""
    await asyncio.sleep(1)
    return {"order_id": order_id, "valid": True}


async def reserve_items(order_id: int) -> dict:
    """Резервирование товаров"""
    await asyncio.sleep(1.5)
    return {"order_id": order_id, "reserved": True}


async def verify_address(order_id: int) -> dict:
    """Проверка адреса доставки"""
    await asyncio.sleep(0.5)
    return {"order_id": order_id, "address_valid": True}


async def process_order_tg(order_id: int) -> dict:
    """Обработка заказа через TaskGroup"""
    results = {}
    async with asyncio.TaskGroup() as group:
        task_1 = group.create_task(validate_order(order_id))
        task_2 = group.create_task(reserve_items(order_id))
        task_3 = group.create_task(verify_address(order_id))

    results["valid"] = task_1.result()
    results["reserved"] = task_2.result()
    results["address_valid"] = task_3.result()
    return results


async def main():
    try:
        result = await process_order_tg(0)
        print(f"Заказ обработан {result}")
    except* ValueError as e:
        for error in e.exceptions:
            print(f"Ошибка валидации {error}")
    except* ConnectionError as e:
        for error in e.exceptions:
            print(f"Ошибка соединения {error}")


asyncio.run(main())
