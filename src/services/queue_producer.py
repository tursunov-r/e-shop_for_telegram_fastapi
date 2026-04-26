import json
import pika


def send_message(queue_name: str, message: dict) -> bool:
    try:
        connection = pika.BlockingConnection(
            pika.ConnectionParameters("localhost")
        )
        channel = connection.channel()
        channel.queue_declare(queue=queue_name, durable=True)
        channel.basic_publish(
            exchange="",
            routing_key=queue_name,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,
            ),
        )
        connection.close()
        return True

    except pika.exceptions.AMQPConnectionError:
        print("Connection to RabitMQ close with error")
        return False
    except Exception as error:
        print(f"Failed to send message to RabitMQ broker: {error}")
        return False
