from datetime import datetime

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from grabber_backend.database_controller.models import (
    Base,
    User,
    Product,
    DatabaseOrder,
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
    def create_order(self, order: DatabaseOrder):
        from pprint import pprint; pprint(order)
        self.session.execute(
            text(
                "SELECT insert_new_order(:user_id, :order_date, :total_cost, :order_status)"
            ),
            {
                "user_id": order.user,
                "order_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_cost": order.total_price,
                "order_status": order.order_status,
            },
        )
        self.session.commit()
