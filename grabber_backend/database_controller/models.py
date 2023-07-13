from sqlalchemy import Column, String, Enum, Numeric, DateTime, ForeignKey, Integer
from sqlalchemy import Column, Integer, String, Date, DECIMAL, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Enum as SQLAlchemyEnum
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from sqlalchemy.dialects.postgresql import ENUM
from enum import Enum as PyEnum

Base = declarative_base()


class UserRoleEnum(PyEnum):
    customer = "customer"
    stock_manager = "stock_manager"


class OrderStatusEnum(PyEnum):
    awaiting_payment = "awaiting_payment"
    pending = "pending"
    processing = "processing"
    ready_to_get = "ready_to_get"
    finished = "finished"
    canceled = "canceled"


class PaymentStatusEnum(PyEnum):
    pending = "pending"
    paid = "paid"
    canceled = "canceled"


class User(Base):
    __tablename__ = "users"
    username = Column(String(50), primary_key=True)
    email = Column(String(50))
    store_name = Column(String(50))
    personal_name = Column(String(50), nullable=False)
    machine_serial_number = Column(String(50))
    phone_number = Column(String(50), unique=True)
    user_role = Column(ENUM(UserRoleEnum), nullable=False)


class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(50))
    product_description = Column(String(300))
    product_price = Column(Numeric(10, 2))
    modified_by_username = Column(String(50), ForeignKey("users.username"))
    modified_at = Column(DateTime)
    user = relationship("User", backref="products")
    weight = Column(Numeric(10, 2))
    size = Column(ENUM("P", "M", "G"))


order_status_type = SQLAlchemyEnum("order_status_type")


class DatabaseOrder(Base):
    __tablename__ = "customer_order"

    customer_order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(128), ForeignKey("users.user_id"))
    order_date = Column(Date)
    total_cost = Column(DECIMAL(10, 2))
    order_status = Column(order_status_type)


class OrderProduct(Base):
    __tablename__ = "order_product"
    order_id = Column(Integer, ForeignKey("customer_order.order_id"), primary_key=True)
    product_id = Column(Integer, ForeignKey("product.product_id"), primary_key=True)
    product_amount = Column(Integer)


class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("customer_order.order_id"))
    payment_date = Column(DateTime)
    payment_method = Column(String(50))
    payment_status = Column(ENUM(PaymentStatusEnum))


class Position(Base):
    __tablename__ = "position"
    position_id = Column(Integer, primary_key=True)
    position_x = Column(Integer)
    position_y = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.product_id"))
    product_amount = Column(Integer)
    modified_by_username = Column(String(50), ForeignKey("users.username"))
    modified_at = Column(DateTime)
    user = relationship("User", backref="positions")
