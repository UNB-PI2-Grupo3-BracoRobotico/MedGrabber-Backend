from time import sleep
from typing import Optional
import logging

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from confluent_kafka import Producer

from grabber_backend.config.kafka import KAFKA_BOOTSTRAP_SERVERS
from grabber_backend.config.database import DATABASE_CONNECTION_STRING
from grabber_backend.database_controller.database_handler import DatabaseHandler
from grabber_backend.database_controller.user import UserDatabaseHandler
from grabber_backend.database_controller.models import User
from grabber_backend.database_controller.product import ProductDatabaseHandler
from grabber_backend.database_controller.models import Product, Position
from grabber_backend.database_controller.position import PositionDatabaseHandler


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


class Product(BaseModel):
    product_id: Optional[int]
    product_name: str
    product_description: str
    product_price: float
    modified_by_username: str
    modified_at: str
    position: Position
    weight: float
    size: str

class Position(BaseModel):
    position_id: Optional[int]
    position_x: int
    position_y: int
    product_id: int
    product_amount: int
    modified_by_username: str
    

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def produce_message(order: Order):
    # Convert Order to JSON and produce to Kafka
    logger.info("Sending order to Kafka")
    producer.produce("create-order", order.json())
    logger.info("Order sent to Kafka")
    producer.flush()


@app.post("/orders/")
async def create_order(order: Order, background_tasks: BackgroundTasks):
    background_tasks.add_task(produce_message, order)
    return {"status": "Order sent"}


@app.post("/users/")
async def create_user(user: User):
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
    logger.info(f"Creating user: {user}")
    try:
        session = db_handler.create_session()
        user_db_handler = UserDatabaseHandler(session)
        status = user_db_handler.insert_user(user)
        logger.info(f"User created: {user}")

    except Exception as e:
        logger.error(f"Failed to create/update user: {e}")
        return {"status": "Failed to create/update user"}, 500

    finally:
        logger.info(f"Closing database session")
        db_handler.close_session(session)

    logger.info(f"Sending response back to client")
    return {"status": f"{status}"}


@app.put("/users/{username}")
async def update_user(username: str, user: User):
    user.username = username
    logger.info(f"Updating user: {user}")
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)

    try:
        logger.info(f"Creating database session")
        session = db_handler.create_session()
        user_db_handler = UserDatabaseHandler(session)
        user_db_handler.upsert_user(user)

    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        return {"status": "Failed to update user"}, 500

    finally:
        db_handler.close_session(session)

    return {"status": "User update request sent"}


@app.post("/products/")
async def create_product(product: Product):
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
    logger.info(f"Creating product: {product}")
    try:
        session = db_handler.create_session()
        product_db_handler = ProductDatabaseHandler(session)

        position_db_handler = PositionDatabaseHandler(session)
        position = Position(
            position_x=product.position.position_x,
            position_y=product.position.position_y,
            product_amount=1,
            modified_by_username=product.modified_by_username,
        )
        status = position_db_handler.insert_position(position)

        product.position = position

        status = product_db_handler.insert_product(product)
        logger.info(f"Product created: {product}")

    except Exception as e:
        logger.error(f"Failed to create/update product: {e}")
        return {"status": "Failed to create/update product"}, 500

    finally:
        logger.info(f"Closing database session")
        db_handler.close_session(session)

    logger.info(f"Sending response back to client")
    return {"status": f"{status}"}


@app.put("/products/{product_id}")
async def update_product(product_id: int, product: Product):
    product.product_id = product_id
    logger.info(f"Updating product: {product}")
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)

    try:
        logger.info(f"Creating database session")
        session = db_handler.create_session()
        product_db_handler = ProductDatabaseHandler(session)
        product_db_handler.update_product(product)

    except Exception as e:
        logger.error(f"Failed to update product: {e}")
        return {"status": "Failed to update product"}, 500

    finally:
        db_handler.close_session(session)

    return {"status": "Product update request sent"}

@app.post("/positions/")
async def create_position(position: Position):
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
    logger.info(f"Creating position: {position}")

    try:
        session = db_handler.create_session()
        position_db_handler = PositionDatabaseHandler(session)
        status = position_db_handler.insert_position(position)
        logger.info(f"Position created: {position}")

    except Exception as e:
        logger.error(f"Failed to create position: {e}")
        return {"status": "Failed to create position"}, 500

    finally:
        logger.info(f"Closing database session")
        db_handler.close_session(session)

    logger.info(f"Sending response back to client")
    return {"status": status}


@app.put("/positions/{position_id}")
async def update_position(position_id: int, position: Position):
    position.position_id = position_id
    logger.info(f"Updating position: {position}")
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)

    try:
        session = db_handler.create_session()
        position_db_handler = PositionDatabaseHandler(session)
        status = position_db_handler.update_position(position)
        logger.info(f"Position updated: {position}")

    except Exception as e:
        logger.error(f"Failed to update position: {e}")
        return {"status": "Failed to update position"}, 500

    finally:
        logger.info(f"Closing database session")
        db_handler.close_session(session)

    logger.info(f"Sending response back to client")
    return {"status": status}