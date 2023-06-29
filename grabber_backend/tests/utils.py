import os
import logging

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from grabber_backend.database_controller.models import User, Product, Order, OrderProduct, Payment, Position, UserRoleEnum
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
import psycopg2
from psycopg2 import sql


TEST_ENGINE_URL = 'postgresql://postgres:pass@db/grabber'

# GET dinamic ddl path
DDL_PATH = os.path.join(os.path.dirname(__file__), '../../', 'database', 'ddl.sql')

# create a new engine and session
# engine = create_engine(TEST_ENGINE_URL)
# Session = sessionmaker(bind=engine)
Base = declarative_base()

engine = None
Session = None


def setup():
    global engine, Session
    # Use the psycopg2 library to connect to the PostgreSQL server
    conn = psycopg2.connect(
        dbname='postgres',
        user='postgres',
        host='db',
        password='pass'
    )

    # Auto-commit must be enabled to create databases
    conn.autocommit = True

    # Open a cursor to perform database operations
    cur = conn.cursor()

    # Use SQL string composition to create a new database
    cur.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('test_db')))

    # Close communication with the database
    cur.close()
    conn.close()

    # Connect to the new test_db database to run migrations
    conn = psycopg2.connect(
        dbname='test_db',
        user='postgres',
        host='db',
        password='pass'
    )
    cur = conn.cursor()

    # Assume you have an DDL SQL file to create all necessary tables
    # and other database structures
    with open(DDL_PATH, 'r') as f:
        cur.execute(f.read())

    # Close communication with the database
    cur.close()
    conn.close()


def teardown():
    global engine
    # Dispose the engine used for test_db and connect to the Postgres server
    engine.dispose()
    engine = create_engine('postgresql://postgres:pass@db:5432/postgres')

    with engine.connect() as connection:
        connection.execution_options(isolation_level="AUTOCOMMIT")
        # Terminate all connections to the test_db
        connection.execute(text('SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = \'test_db\' AND pid <> pg_backend_pid()'))

        # Drop the test_db
        connection.execute(text('DROP DATABASE test_db'))

