from sqlalchemy import text
from sqlalchemy.orm import Session
from src.core.db_connect import engine


def users_table_analyze():
    with Session(engine) as session:
        result = session.execute(
            text("""EXPLAIN ANALYZE SELECT * FROM users WHERE id = :uid"""),
            {"uid": 1},
        )
        for row in result:
            print(row[0])


def products_table_analyze():
    with Session(engine) as session:
        result = session.execute(
            text("""EXPLAIN ANALYZE SELECT * FROM products WHERE id = :uid"""),
            {"uid": 1},
        )
        for row in result:
            print(row[0])


def orders_table_analyze():
    with Session(engine) as session:
        result = session.execute(
            text("""EXPLAIN ANALYZE SELECT * FROM orders WHERE id = :uid"""),
            {"uid": 1},
        )
        for row in result:
            print(row[0])


def order_items_table_analyze():
    with Session(engine) as session:
        result = session.execute(
            text(
                """EXPLAIN ANALYZE SELECT * FROM order_items WHERE order_id = :uid"""
            ),
            {"uid": 1},
        )
        for row in result:
            print(row[0])


users_table_analyze()
products_table_analyze()
orders_table_analyze()
order_items_table_analyze()
