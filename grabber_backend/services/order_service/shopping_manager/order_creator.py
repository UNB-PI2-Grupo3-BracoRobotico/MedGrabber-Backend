import logging

from ..models import Order
from grabber_backend.database_controller.models import OrderStatusEnum
from grabber_backend.database_controller.order import OrderDatabaseHandler


class OrderCreator:
    def __init__(self, order, session):
        self.logger = logging.getLogger(__name__)
        self.order = order
        self.session = session

    def validate_order(self, order):
        self.logger.info("Validating order")

        order = Order(**order)

        return order

    def create_order(self, order, user_id):
        self.logger.info("Creating order in database")
        db_handler = OrderDatabaseHandler(self.session)
        order_id = db_handler.create_order(order, user_id)
        self.logger.info(f"Order created in database: id {order_id}")
        return order_id

    def receive_order(self):
        if order := self.validate_order(self.order):
            order_id = self.create_order(order)
            return OrderStatusEnum.created, order_id
        else:
            self.logger.info("Order is not valid")
            return OrderStatusEnum.canceled, None
