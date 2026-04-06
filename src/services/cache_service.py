import datetime
import json
import redis
from src.database.queries import (
    get_all_products_from_db_query,
    update_product_in_db_query,
    get_product_by_id_from_db_query,
)
from src.session.generate_session import generate_user_session

redis_client = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True
)


async def get_cached_products():
    cache = redis_client.get("products:all")
    if cache:
        return json.loads(await cache)
    products = await get_all_products_from_db_query()
    result = await redis_client.setex(
        "products:all", 3600, json.dumps(products)
    )
    return result


async def update_product(product_id, data):
    await update_product_in_db_query(product_id, data)
    await redis_client.delete(f"products:{product_id}")
    await redis_client.delete("products:all")


async def get_cached_by_id(product_id):
    cache = await redis_client.get(f"products:{product_id}")
    if cache:
        return json.loads(cache)
    products = await get_product_by_id_from_db_query(product_id)
    result = await redis_client.setex(
        f"products:{product_id}", 3600, json.dumps(products)
    )
    return result


def create_user_session(user_id):
    session_token = generate_user_session()
    session_data = {
        "user_id": user_id,
        "session_token": session_token,
        "created_at": datetime.datetime.now().isoformat(),
    }

    redis_client.setex(
        f"users:{session_token}", 86400, json.dumps(session_data)
    )
    return session_data


async def get_user_session(session_token):
    session = await redis_client.get(f"users:{session_token}")
    if session:
        return json.loads(session)
    return None


def delete_user_session(session_token):
    session = redis_client.get(f"users:{session_token}")
    if session:
        redis_client.delete(f"users:{session_token}")


print(f"All products in cache: {get_cached_products()}")
print(f"Get product by id in cache {get_cached_by_id(1)}")
print(create_user_session(1))
