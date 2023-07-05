from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from grabber_backend.database_controller.models import (
    Base,
    User,
    Product,
    Order,
    OrderProduct,
    Payment,
    Position,
    UserRoleEnum,
    OrderStatusEnum,
    PaymentStatusEnum,
)


class OrderDatabaseHandler:
    def __init__(self, session):
        self.session = session

    # Call the stored procedure to create an order
    def create_order(self, order: Order):
        self.session.execute(
            text(
                "SELECT create_order(:user_id, :order_date, :total_cost, :order_status)"
            ),
            {
                "user_id": order.user_id,
                "order_date": order.order_date,
                "total_cost": order.total_cost,
                "order_status": order.order_status,
            },
        )
        self.session.commit()
