import os
import logging
from pathlib import Path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from grabber_backend.database_controller.models import (
    User,
    Product,
    Order,
    OrderProduct,
    Payment,
    Position,
    UserRoleEnum,
)
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2 import sql


TEST_ENGINE_URL = "postgresql://postgres:pass@db/grabber"

# GET dinamic ddl path
DDL_LIST = Path(os.path.join(os.path.dirname(__file__), "../../", "database")).glob('*')


import psycopg2
import pytest
import os

import psycopg2
import pytest

# Set up a test data for each test
@pytest.fixture(scope='function')
def setup_db():
    conn = psycopg2.connect(
        dbname='grabber',
        user='postgres',
        password='pass',
        host='db',  # this should be the service name from your docker-compose file
        port=5432,
    )
    cur = conn.cursor()

    # Add your setup SQL commands here, for example:
    # cur.execute("INSERT INTO my_table (column1, column2) VALUES ('test_data1', 'test_data2')")

    conn.commit()

    yield conn

    # Add your teardown SQL commands here, for example:
    # cur.execute("DELETE FROM my_table WHERE column1 = 'test_data1' and column2 = 'test_data2'")

    conn.commit()
    cur.close()
    conn.close()

# Test your stored procedures
def test_stored_procedure(setup_db):
    cur = setup_db.cursor()
    cur.callproc('name_of_stored_procedure', [param1, param2])  # replace with your actual procedure name and params
    result = cur.fetchone()
    assert result == expected_result  # replace with your expected result
