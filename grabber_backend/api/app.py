from time import sleep
from typing import Optional
import logging

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from confluent_kafka import Producer

from grabber_backend.config.kafka import KAFKA_BOOTSTRAP_SERVERS
from grabber_backend.database_controller.database_handler import DatabaseHandler
from grabber_backend.database_controller.User_database_handler import UserDatabaseHandler

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

# Criar uma instância do DatabaseHandler
db_handler = DatabaseHandler()

# Criar uma instância do UserDatabaseHandler, passando o DatabaseHandler
user_db_handler = UserDatabaseHandler(db_handler)

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

@app.post("/users/")
async def create_update_user(user: User):
    # Chamar o método de inserção/atualização do UserDatabaseHandler
    user_db_handler.upsert_user(user)
    return {"status": "User creation/update request sent"}



@app.put("/users/{username}")
async def update_user(username: str, user: User):
    # Set the username to the path parameter
    user.username = username
    # Chamar o método de inserção/atualização do UserDatabaseHandler
    user_db_handler.upsert_user(user)
    return {"status": "User update request sent"}