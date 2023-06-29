from sqlalchemy import (
    Column,
    Integer,
    String,
    Enum,
    Date,
    ForeignKey,
    Numeric,
    TIMESTAMP,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class UserRoleEnum(Enum):
    customer = "customer"
    stock_manager = "stock_manager"


class OrderStatusEnum(Enum):
    created = "created"
    pending = "pending"
    paid = "paid"
    separation = "separation"
    delivered = "delivered"
    canceled = "canceled"


class PaymentStatusEnum(Enum):
    pending = "pending"
    paid = "paid"
    canceled = "canceled"


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hash = Column(String)
    email = Column(String)
    store_name = Column(String)
    personal_name = Column(String)
    machine_serial_number = Column(String)
    phone_number = Column(String)
    user_role = Column(Enum('customer', 'stock_manager', name='user_role_type'))


class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column(String)
    product_description = Column(String)
    product_price = Column(Numeric)
    modified_by = Column(Integer, ForeignKey("users.user_id"))
    modified_at = Column(TIMESTAMP)


class Order(Base):
    __tablename__ = "customer_order"

    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    order_date = Column(Date)
    total_cost = Column(Numeric)
    order_status = Column(OrderStatusEnum)


class OrderProduct(Base):
    __tablename__ = "order_product"

    customer_order_id = Column(
        Integer, ForeignKey("customer_order.order_id"), primary_key=True
    )
    product_id = Column(Integer, ForeignKey("product.product_id"), primary_key=True)
    product_amount = Column(Integer)


class Payment(Base):
    __tablename__ = "payment"

    payment_id = Column(Integer, primary_key=True)
    customer_order_id = Column(Integer, ForeignKey("customer_order.order_id"))
    payment_date = Column(Date)
    payment_method = Column(String)
    payment_status = Column(PaymentStatusEnum)


class Position(Base):
    __tablename__ = "position"

    position_id = Column(Integer, primary_key=True)
    position_x = Column(Integer)
    position_y = Column(Integer)
    product_id = Column(Integer, ForeignKey("product.product_id"))
    product_amount = Column(Integer)
    modified_by = Column(Integer, ForeignKey("users.user_id"))
    modified_at = Column(TIMESTAMP)
