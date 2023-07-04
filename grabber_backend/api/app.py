from time import sleep
from typing import Optional
import logging

from fastapi import FastAPI
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

class User(BaseModel):
    username: str
    password_hash: str
    email: str
    store_name: str
    personal_name: str
    machine_serial_number: str
    phone_number: str
    user_role: str
    
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/orders/")
async def create_order(order: Order):
    # Convert Order to JSON and produce to Kafka
    producer.produce("create-order", order.json())
    producer.flush()
    return {"status": "Order sent"}

@app.post("/users/")
async def create_update_user(user: User):
    # Convert User to JSON and produce to Kafka
    producer.produce("upsert-user", user.json())
    producer.flush()
    return {"status": "User creation/update request sent"}


@app.put("/users/{username}")
async def update_user(username: str, user: User):
    # Set the username to the path parameter
    user.username = username
    # Convert User to JSON and produce to Kafka
    producer.produce("upsert-user", user.json())
    producer.flush()
    return {"status": "User update request sent"}