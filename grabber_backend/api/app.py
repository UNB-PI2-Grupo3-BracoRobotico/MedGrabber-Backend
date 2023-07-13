from time import sleep
from typing import Optional, List
import logging
from datetime import datetime

from fastapi import FastAPI, BackgroundTasks, HTTPException, status
from pydantic import BaseModel
from confluent_kafka import Producer
from sqlalchemy import text

from grabber_backend.config.kafka import KAFKA_BOOTSTRAP_SERVERS
from grabber_backend.config.database import DATABASE_CONNECTION_STRING
from grabber_backend.database_controller.database_handler import DatabaseHandler
from grabber_backend.database_controller.user import UserDatabaseHandler
from grabber_backend.database_controller.models import User
from grabber_backend.database_controller.product import ProductDatabaseHandler
from grabber_backend.database_controller.position import PositionDatabaseHandler
from grabber_backend.database_controller.models import Product, Position
from grabber_backend.database_controller.order import OrderDatabaseHandler


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


class OrderItem(BaseModel):
    product_id: int
    amount: int
    price: float


class ApiOrder(BaseModel):
    customer_order_id: Optional[int] = None
    user: str
    order_items: List[OrderItem]
    total_price: float
    payment_method: str
    order_date: Optional[datetime] = None
    order_status: Optional[str] = "awaiting_payment"


class User(BaseModel):
    firebase_uid: str
    email: str
    store_name: str
    machine_serial_number: str
    phone_number: str


class UserUpdate(BaseModel):
    email: str = None
    store_name: str = None
    machine_serial_number: str = None
    phone_number: str = None


class ProductPosition(BaseModel):
    product_name: str
    product_description: str
    product_price: float
    peso: float
    size: str
    modified_by_user: str
    position_x: int
    position_y: int
    amount: int


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def produce_message(order: ApiOrder):
    # Convert Order to JSON and produce to Kafka
    logger.info("Sending order to Kafka")
    producer.produce("create-order", order.json())
    logger.info("Order sent to Kafka")
    producer.flush()


@app.post("/orders/")
async def create_order(order: ApiOrder, background_tasks: BackgroundTasks):
    background_tasks.add_task(produce_message, order)
    return {"status": "Order sent"}


@app.get("/orders/")
async def get_orders():
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
    orders = []
    try:
        session = db_handler.create_session()
        order_db_handler = OrderDatabaseHandler(session)

        orders = order_db_handler.get_orders()
    except Exception as e:
        logger.error(f"Failed to get orders: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get orders - {e}")
    finally:
        logger.info(f"Closing database session")
        db_handler.close_session(session)
    return {"orders": orders}


@app.post("/users/", status_code=status.HTTP_201_CREATED)
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
        raise HTTPException(status_code=500, detail=f"user creation failed - {e}")

    finally:
        logger.info(f"Closing database session")
        db_handler.close_session(session)

    logger.info(f"Sending response back to client")
    if status == "failed":
        raise HTTPException(status_code=409, detail="user creation failed")
    return {"message": "user created"}


# TODO - This has to be a patch request
# TODO - Instead of username we must pass the uid from the user
# TODO - We shouldn't pass the whole user to this endpoint just the properties we want to change


@app.patch("/users/{user_id}", status_code=204)
async def update_user(user_id: str, user: UserUpdate):
    logger.info(f"Updating user: {user}")
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)

    try:
        logger.info(f"Creating database session")
        session = db_handler.create_session()
        user_db_handler = UserDatabaseHandler(session)
        status = user_db_handler.update_user(user_id, user)
        logger.info(f"User updated: {user}")

    except Exception as e:
        logger.error(f"Failed to update user: {e}")
        raise HTTPException(status_code=500, detail="Failed to update user")

    finally:
        db_handler.close_session(session)
    logger.info(f"Sending response back to client")
    if status == "failed":
        raise HTTPException(status_code=409, detail="User update failed")
    return {"message": "User updated"}


@app.get("/users/{user_id}", response_model=UserUpdate)
async def get_user(user_id: str):
    logger.info(f"Fetching user with user_id: {user_id}")
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)

    try:
        logger.info(f"Creating database session")
        session = db_handler.create_session()
        user_db_handler = UserDatabaseHandler(session)
        user = user_db_handler.get_user(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

    except Exception as e:
        logger.error(f"Failed to fetch user: {e}")
        raise HTTPException(status_code=500, detail="Failed to fetch user")

    finally:
        db_handler.close_session(session)
    logger.info(f"Sending response back to client")
    if isinstance(user, dict):
        return UserUpdate(**user)
    else:
        return user


@app.get("/availablePositions/")
async def get_available_positions():
    try:
        db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
        logger.info(f"Creating database session")
        session = db_handler.create_session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to access database!")
    position_db_handler = PositionDatabaseHandler(session)
    available_positions = position_db_handler.get_available_positions()
    logger.info(f"Closing database session")
    db_handler.close_session(session)
    logger.info(f"Sending response back to client")
    return {"available_positions": available_positions}


@app.get("/products/")
async def get_product_with_position():
    try:
        db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
        session = db_handler.create_session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to access database!")
    product_db_handler = ProductDatabaseHandler(session)
    filled_positions = product_db_handler.get_products()
    db_handler.close_session(session)
    
    return {"products": filled_positions}


@app.post("/products/", status_code=201)
async def create_product(product: ProductPosition):
    try:
        db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
        session = db_handler.create_session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to access database!")
    
    product_db_handler = ProductDatabaseHandler(session)
    logger.info(f"Creating product: {product}")
    message = product_db_handler.insert_product(product)
    logger.info(f"Product created: {product}")
    logger.info(f"Closing database session")
    db_handler.close_session(session)
    logger.info(f"Sending response back to client")
    return {"message": message}


@app.delete("/products/{product_id}")
async def delete_product(product_id: int, status_code=status.HTTP_200_OK):
    try:
        db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
        session = db_handler.create_session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to access database!")
    product_db_handler = ProductDatabaseHandler(session)
    logger.info(f"Deleting product with ID: {product_id}")
    message = product_db_handler.delete_product(product_id)
    logger.info(f"Product deleted with ID: {product_id}")
    logger.info(f"Closing database session")
    db_handler.close_session(session)

    return {"message": message}


@app.put("/products/{product_id}")
async def update_product(product_id: int, updated_product: ProductPosition):
    try:
        db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
        session = db_handler.create_session()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=f"Failed to access database!")
    
    product_db_handler = ProductDatabaseHandler(session)
    message = product_db_handler.update_product(product_id, updated_product)
    logger.info(f"Product updated with ID: {product_id}")

    logger.info(f"Closing database session")
    db_handler.close_session(session)
    logger.info(f"Sending response back to client")
    return {"message": message}
