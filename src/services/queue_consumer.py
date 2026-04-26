import json
import pika
import time

from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.product_repository import ProductRepository
from src.services.send_notification_service import NotificationService


class QueueConsumer:
    def __init__(self, host: str = "localhost"):
        self.host = host
        self.connection = None
        self.channel = None
        self.max_retries = 3
        self.retry_count = 0

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue="order_processing", durable=True)
            self.channel.queue_declare(
                queue="order_processing_errors", durable=False
            )
            self.channel.basic_qos(prefetch_count=1)
            return True
        except Exception as e:
            print(f"RebitMQ connection error: {e}")
            return False

    def process_message(
        self, ch, method, properties, body, session: AsyncSession
    ):
        try:
            message = json.loads(body)
            task = message.get("task")
            order_id = message.get("order_id")

            retry_count = (
                properties.headers.get("x-retry-count", 0)
                if properties.headers
                else 0
            )

            # Обработка задачи
            if task == "send_email":
                user_email = message.get("user_email")
                notification = NotificationService()
                notification.send_email(
                    user_email, f"Order {order_id} created"
                )
                print(notification)

            elif task == "update_stock":
                items = message.get("items", [])
                ProductRepository.update_product_quantity(
                    product_id=items[0], quantity=items[1], session=session
                )

                # Успешная обработка
                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(f"Task {task} for order {order_id} done")
        except Exception as e:
            print(f"RebitMQ processing error: {e}")
            if self.retry_count < self.max_retries:
                self.retry_count += 1
                delay = 2**self.retry_count
                print(
                    f"Retry {self.retry_count}/{self.max_retries} after {delay} seconds..."
                )
                time.sleep(delay)

                ch.basic_publish(
                    exchange="",
                    routing_key="order_processing",
                    body=body,
                    properties=pika.BasicProperties(
                        delivery_mode=2,
                        headers={"x-retry-count": self.retry_count},
                    ),
                )
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
            else:
                # Отправка в очередь ошибок
                ch.basic_publish(
                    exchange="",
                    routing_key="order_processing_errors",
                    body=body,
                    properties=pika.BasicProperties(delivery_mode=2),
                )

                ch.basic_ack(delivery_tag=method.delivery_tag)
                print(
                    f"Task send to stack after {self.max_retries} retries..."
                )

    def start_consumer(self):
        if not self.connection:
            return
        self.channel.basic_consume(
            queue="order_processing",
            on_message_callback=self.process_message,
        )
        print(
            "Consumer started and waiting for messages from order_processing..."
        )
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()
            self.connection.close()


if __name__ == "__main__":
    consumer = QueueConsumer()
    consumer.start_consumer()
