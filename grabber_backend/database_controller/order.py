from datetime import datetime
import logging


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

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class OrderDatabaseHandler:
    def __init__(self, session):
        self.session = session

    # Call the stored procedure to create an order
    def create_order(self, order: DatabaseOrder):
        from pprint import pprint; pprint(order)
        result = self.session.execute(
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
        
        order_id = result.fetchone()[0]

        self.session.commit()

        pprint(f'ID DO PEDIDO: {order_id}')

        for product in order.order_items:
            logger.info(product)
            self.session.execute(
                text(
                    """
                    CALL insert_order_product_and_update_position(:order_id, :product_id, :product_amount, :user_id);
                    """
                ),
                {
                    "product_id": product["product_id"],
                    "product_amount": product["amount"],
                    "order_id": order_id,
                    "user_id": order.user,
                },
                

            )

        self.session.commit()

        return order_id
