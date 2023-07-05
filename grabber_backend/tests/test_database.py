import os
from pathlib import Path

import psycopg2
import pytest
from grabber_backend.database_controller.models import (
    User,
    Product,
    Order,
    OrderProduct,
    Payment,
    Position,
    UserRoleEnum,
)

TEST_ENGINE_URL = "postgresql://postgres:pass@db/grabber"

DDL_LIST = Path(os.path.join(os.path.dirname(__file__), "../../", "database")).glob("*")


@pytest.fixture(scope="function")
def setup_db():
    conn = psycopg2.connect(
        dbname="grabber",
        user="postgres",
        password="pass",
        host="db",
        port=5432,
    )
    cur = conn.cursor()

    conn.commit()

    yield conn

    conn.commit()
    cur.close()
    conn.close()


# def test_stored_procedure(setup_db):
#     username = "test_username"
#     password_hash = "test_pasword"
#     email = "test_email@gmail.com"
#     store_name = "test_store_name"
#     name = "Test Name"
#     machine_serial = "901248210941208"
#     phone_number = "1234567890"
#     user_role = "stock_manager"

#     cur = setup_db.cursor()
#     try:
#         cur.callproc(
#             "insert_new_user",
#             [
#                 username,
#                 password_hash,
#                 email,
#                 store_name,
#                 name,
#                 machine_serial,
#                 phone_number,
#                 user_role,
#             ],
#         )
#         result = cur.fetchone()

#         # query user
#         cur.execute("SELECT phone_number FROM users WHERE username = %s", (username,))
#         user = cur.fetchone()

#         assert user[0] == phone_number
#     finally:
#         cur.execute("DELETE FROM users WHERE username = %s", (username,))
#         cur.close()
