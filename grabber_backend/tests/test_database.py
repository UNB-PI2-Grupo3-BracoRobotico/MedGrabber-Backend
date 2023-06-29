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

from grabber_backend.tests.utils import setup, teardown


def test_user():
    # setup()

    session = Session()

    new_user = User(
        username='test_user',
        password_hash='test_hash',
        personal_name='Test User',
        user_role=UserRoleEnum.customer,
        phone_number='123456789'
    )
    session.add(new_user)
    session.commit()

    user = session.query(User).filter_by(username='test_user').first()
    assert user is not None

    session.close()

    teardown()