import datetime
import json
import redis
from psycopg_learn.src.database.queries import (
    get_all_products_from_db,
    update_product_in_db,
    get_product_by_id_from_db,
)
from psycopg_learn.src.session.generate_session import generate_user_session


redis_client = redis.Redis(
    host="localhost", port=6379, db=0, decode_responses=True
)


def get_cached_products():
    cache = redis_client.get("products:all")
    if cache:
        return json.loads(cache)
    products = get_all_products_from_db()
    redis_client.setex("products:all", 3600, json.dumps(products))


def update_product(product_id, data):
    update_product_in_db(product_id, data)
    redis_client.delete(f"products:{product_id}")
    redis_client.delete("products:all")


def get_cached_by_id(product_id):
    cache = redis_client.get(f"products:{product_id}")
    if cache:
        return json.loads(cache)
    products = get_product_by_id_from_db(product_id)
    redis_client.setex(f"products:{product_id}", 3600, json.dumps(products))


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


def get_user_session(session_token):
    session = redis_client.get(f"users:{session_token}")
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
