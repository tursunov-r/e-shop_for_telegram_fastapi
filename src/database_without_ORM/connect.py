import os

import psycopg2
from dotenv import load_dotenv
from contextlib import contextmanager


load_dotenv()


DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "database": os.getenv("DB_NAME"),
}


@contextmanager
def get_connection():
    with psycopg2.connect(**DB_CONFIG) as connection:
        try:
            yield connection
        except Exception as e:
            raise e


def try_connect():
    with get_connection() as connection:
        print(connection)
        print({"message": "Connected"})


if __name__ == "__main__":
    try_connect()
