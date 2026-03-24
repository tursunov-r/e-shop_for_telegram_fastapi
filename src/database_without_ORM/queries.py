"""Транзакция это процесс соединения с базой данных, при котором выполняются манипуляции с данными, выборка, добавление, обновление или удаление строки. Атомарность - это условие при котором транзакция выолняется полностью, или не выполняется вовсе. Согласованность - проверка условий, например перед выполнением коммита необходимо проверить достаточно ли на складе товаров, если их меньше чем в транзакции, вызываем исключение, в последствии которого выполняется rollback. Изоляция - используется для того, что бы транзакции не мешали друг другу. Гарантия - гарантирут сохранность данных."""

import datetime

import psycopg2
from psycopg_learn.src.database_without_ORM.connect import get_connection


def create_order(user_id, product_id, quantity, total):
    with get_connection() as connection:
        connection.set_isolation_level(
            psycopg2.extensions.ISOLATION_LEVEL_SERIALIZABLE
        )
        with connection.cursor() as cursor:
            try:
                cursor.execute(
                    "SELECT balance FROM users WHERE id = %s", (user_id,)
                )
                user = cursor.fetchone()[0]
                if not user or user < total:
                    raise Exception("Not enough balance")
                cursor.execute(
                    "SELECT quantity FROM products WHERE id = %s",
                    (product_id,),
                )
                product = cursor.fetchone()[0]
                if not product or product < quantity:
                    raise Exception("Not enough quantity")
                cursor.execute(
                    "INSERT INTO orders (user_id, total, created_at) VALUES (%s, %s, %s) RETURNING id",
                    (user_id, total, datetime.datetime.now()),
                )
                order_id = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT price FROM products WHERE id = %s", (product_id,)
                )
                price = cursor.fetchone()[0]
                cursor.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, total) VALUES (%s, %s, %s, %s)",
                    (order_id, product_id, quantity, price * quantity),
                )
                cursor.execute(
                    "UPDATE users SET balance = balance - %s WHERE id = %s",
                    (total, user_id),
                )
                cursor.execute(
                    "UPDATE products SET quantity = quantity - %s WHERE id = %s",
                    (quantity, product_id),
                )
                connection.commit()
                return order_id

            except Exception as e:
                connection.rollback()
                raise e


print(create_order(1, 1, 2, 2000))
