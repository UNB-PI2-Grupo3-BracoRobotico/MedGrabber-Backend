from time import sleep
from typing import Optional
import logging

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from confluent_kafka import Producer

from grabber_backend.config.kafka import KAFKA_BOOTSTRAP_SERVERS

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MAX_RETRIES = 5

for retry in range(MAX_RETRIES):
    try:
        sleep(5)
        logger.info("Starting Kafka producer")
        conf = {"bootstrap.servers": KAFKA_BOOTSTRAP_SERVERS}
        producer = Producer(conf)
        break
    except Exception as e:
        logger.error(f"Failed to start Kafka producer: {e}, trying again... {retry}")
else:
    logger.error("Failed to start Kafka producer, exiting...")
    exit(1)


class Order(BaseModel):
    id: Optional[int]
    user: str
    order_items: list
    total_price: float
    payment_method: str


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def produce_message(order: Order):
    # Convert Order to JSON and produce to Kafka
    logger.info('Sending order to Kafka')
    producer.produce("create-order", order.json())
    logger.info('Order sent to Kafka')
    producer.flush()

@app.post("/orders/")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    background_tasks.add_task(produce_message, order)
    return {"status": "Order sent"}
