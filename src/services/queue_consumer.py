import json
import pika
import time
from functools import partial


def process_message_with_retry(ch, method, properties, body, max_retries=3):
    message = json.loads(body)
    task = message.get("task")
    order_id = message.get("order_id")

    retry_count = (
        properties.headers.get("x-retry-count", 0) if properties.headers else 0
    )
    try:
        if task == "process_order":
            process_order = order_id
            ch.basic_ack(delivery_tag=method.delivery_tag)
            print(f"Order {order_id} successfully processed")

    except Exception as ex:
        print(f"Exception while processing {order_id}: {ex}")
        if retry_count < max_retries:
            retry_count += 1
            delay = 2**retry_count

            print(
                f"Retrying {retry_count}/{max_retries} after {delay} seconds"
            )
            time.sleep(delay)
            ch.basic_publish(
                exchange="",
                routing_key=task,
                properties=pika.BasicProperties(
                    delivery_mode=2,
                    headers={"x-retry-count": retry_count},
                ),
            )
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
        else:
            print(
                f"All retries failed for task: {task} order: {order_id}, send to errors stack"
            )
            ch.basic_publish(
                exchange="",
                routing_key=f"{task}_errors",
                body=body,
                properties=pika.BasicProperties(delivery_mode=2),
            )
            ch.basic_nack(delivery_tag=method.delivery_tag)


def start_consumer_with_retry(queue_name, max_retries: int = 3):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters("localhost")
    )
    channel = connection.channel()
    channel.queue_declare(queue=queue_name, durable=True)

    callback = partial(process_message_with_retry, max_retries=max_retries)
    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
    )
    print(f"Waiting for messages in stack {queue_name}")
    channel.start_consuming()


start_consumer_with_retry("process_order", max_retries=3)
