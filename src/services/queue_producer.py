import json
import pika


class QueueProducer:
    def __init__(self, queue_name: str, host: str = "localhost"):
        self.queue_name = queue_name
        self.host = host
        self.connection = None
        self.channel = None

    def connect(self) -> bool:
        try:
            self.connection = pika.BlockingConnection(
                pika.ConnectionParameters(self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name, durable=True)

            return True

        except Exception as error:
            print(f"Failed to send message to RabitMQ broker: {error}")
            return False

    def send_order_task(
        self, order_id: int, task_type: str, data: dict
    ) -> bool:
        if not self.channel:
            if not self.connect():
                return False
        try:
            message = {"task": task_type, "order_id": order_id, **data}
            self.channel.basic_publish(
                exchange="",
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                ),
            )
            print(f"Sent task to RabitMQ broker: {message}")
            return True
        except Exception as error:
            print(f"Failed to send message to RabitMQ broker: {error}")
            return False

    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
