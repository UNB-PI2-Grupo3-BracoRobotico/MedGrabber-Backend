from time import sleep
from typing import Optional, List
import logging

from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from confluent_kafka import Producer
from sqlalchemy import text

from grabber_backend.config.kafka import KAFKA_BOOTSTRAP_SERVERS
from grabber_backend.config.database import DATABASE_CONNECTION_STRING
from grabber_backend.database_controller.database_handler import DatabaseHandler
from grabber_backend.database_controller.user import UserDatabaseHandler
from grabber_backend.database_controller.models import User
from grabber_backend.database_controller.product import ProductDatabaseHandler
from grabber_backend.database_controller.models import Product, Position


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
        logger.error(
            f"Failed to start Kafka producer: {e}, trying again... {retry}")
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


class ProductPosition(BaseModel):
    product_name: str
    product_description: str
    product_price: float
    peso: float
    size: str
    modified_by_username: str
    position_x: int
    position_y: int
    product_amount: int


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


@app.get("/orders/")
async def get_orders():
    # TODO: Implement actual database query

    # TODO: Define possible status for order - Must be (awaiting payment, pending, processing, ready to get, finished)
    # make them as they are here but in snake_case - (awaiting_payment, pending, processing, ready_to_get, finished)

    # TODO: Insert proper dating format

    # TODO: order_items are missing description
    return {
        "orders": [
            {
                "id": 1,
                "user": "bobross",
                "order_items": [
                    {
                        "id": 1,
                        "name": "Caixa de Papelão",
                        "price": 10.0,
                        "quantity": 2,
                        "position_x": 0,
                        "position_y": 1,
                        "size": "M",
                        "weight": 0.5,
                    },
                    {
                        "id": 2,
                        "name": "Livro: Python for Dummies",
                        "price": 20.0,
                        "quantity": 1,
                        "position_x": 0,
                        "position_y": 0,
                        "size": "M",
                        "weight": 0.3,
                    },
                ],
                "total_price": 40.0,
                "payment_method": "pix",
                "status": "pending",
                "date": 1688922791,
            },
            {
                "id": 2,
                "user": "johndoe",
                "order_items": [
                    {
                        "id": 3,
                        "name": "Controle Logitech",
                        "price": 30.0,
                        "quantity": 1,
                        "position_x": 1,
                        "position_y": 0,
                        "size": "P",
                        "weight": 0.2,
                    },
                    {
                        "id": 4,
                        "name": "Mouse Bluetooth",
                        "price": 40.0,
                        "quantity": 3,
                        "position_x": 0,
                        "position_y": 1,
                        "size": "M",
                        "weight": 0.3,
                    },
                ],
                "total_price": 150.0,
                "payment_method": "pix",
                "status": "finished",
                "date": 1594314791,
            },
            {
                "id": 2,
                "user": "johndoe",
                "order_items": [
                    {
                        "id": 5,
                        "name": "Licor Baileys",
                        "price": 100.0,
                        "quantity": 6,
                        "position_x": 0,
                        "position_y": 2,
                        "size": "G",
                        "weight": 1.0,
                    },
                    {
                        "id": 4,
                        "name": "Mouse Bluetooth",
                        "price": 40.0,
                        "quantity": 1,
                        "position_x": 2,
                        "position_y": 2,
                        "size": "P",
                        "weight": 0.3,
                    },
                ],
                "total_price": 640.0,
                "payment_method": "pix",
                "status": "ready_to_get",
                "date": 1594833191,
            },
        ]
    }


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


@app.get("/storage/")
async def get_storage():
    return {
        "storage": [
            {
                "id": 1,
                "name": "Caixa de Papelão",
                "description": "Caixa de papelão para transporte de objetos",
                "price": 10.0,
                "quantity": 10,
                "position_x": 0,
                "position_y": 0,
                "size": "M",
                "weight": 0.5,
            },
            {
                "id": 2,
                "name": "Livro: Python for Dummies",
                "description": "Livro de Python para iniciantes",
                "price": 20.0,
                "quantity": 5,
                "position_x": 0,
                "position_y": 1,
                "size": "M",
                "weight": 0.3,
            },
            {
                "id": 3,
                "name": "Controle Logitech",
                "description": "Controle de submarino",
                "price": 30.0,
                "quantity": 2,
                "position_x": 1,
                "position_y": 0,
                "size": "P",
                "weight": 0.2,
            },
            {
                "id": 4,
                "name": "Mouse Bluetooth",
                "description": "Mouse sem fio",
                "price": 40.0,
                "quantity": 10,
                "position_x": 1,
                "position_y": 1,
                "size": "M",
                "weight": 0.1,
            },
            {
                "id": 5,
                "name": "Licor Baileys",
                "description": "Licor de chocolate",
                "price": 100.0,
                "quantity": 10,
                "position_x": 2,
                "position_y": 0,
                "size": "G",
                "weight": 1.0,
            },
        ],
        "available_positions": [
            {
                "position_x": 2,
                "position_y": 2,
            },
            {
                "position_x": 2,
                "position_y": 1,
            },
            {
                "position_x": 1,
                "position_y": 2,
            },
            {
                "position_x": 0,
                "position_y": 2,
            },
        ],
    }


@app.post("/products/")
async def create_product(product: ProductPosition):
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
    logger.info(f"Creating product: {product}")
    try:
        session = db_handler.create_session()
        product_db_handler = ProductDatabaseHandler(session)

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


class ProductPositionData(BaseModel):
    product_id: Optional[int]
    product_name: Optional[str]
    product_description: Optional[str]
    product_price: Optional[float]
    peso: Optional[float]
    size: Optional[str]
    position_x: int
    position_y: int


@app.get("/products/")
async def get_product_position_list():
    db_handler = DatabaseHandler(DATABASE_CONNECTION_STRING)
    with db_handler.create_session() as connection:
        # Query for all products with filled positions.
        result_filled_positions = connection.execute(
            text(
                """
            SELECT 
                p.product_id,
                p.product_name,
                p.product_description,
                p.product_price,
                p.peso,
                p.size,
                pos.position_x,
                pos.position_y
            FROM 
                position pos
            JOIN 
                product p 
            ON 
                pos.product_id = p.product_id
            WHERE 
                pos.is_exit = FALSE;
        """
            )
        )

        filled_positions = [
            {
                "product_id": row[0],
                "product_name": row[1],
                "product_description": row[2],
                "product_price": row[3],
                "peso": row[4],
                "size": row[5],
                "position_x": row[6],
                "position_y": row[7],
            }
            for row in result_filled_positions
        ]

        # Query for all empty positions.
        result_empty_positions = connection.execute(
            text(
                """
            SELECT 
                NULL AS product_id,
                NULL AS product_name,
                NULL AS product_description,
                NULL AS product_price,
                NULL AS peso,
                NULL AS size,
                pos.position_x,
                pos.position_y
            FROM 
                position pos
            WHERE 
                pos.product_id IS NULL AND 
                pos.is_exit = FALSE;
        """
            )
        )

        empty_positions = [
            {
                "product_id": row[0],
                "product_name": row[1],
                "product_description": row[2],
                "product_price": row[3],
                "peso": row[4],
                "size": row[5],
                "position_x": row[6],
                "position_y": row[7],
            }
            for row in result_empty_positions
        ]

    return {"products": filled_positions, "available_positions": empty_positions}
