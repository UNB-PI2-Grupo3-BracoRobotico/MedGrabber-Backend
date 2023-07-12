import logging

from ..models import ServiceOrder
from grabber_backend.database_controller.models import OrderStatusEnum
from grabber_backend.database_controller.order import OrderDatabaseHandler


class OrderCreator:
    def __init__(self, order, session):
        self.logger = logging.getLogger(__name__)
        self.order = order
        self.session = session

    def validate_order(self, order):
        self.logger.info("Validating order")

        order = ServiceOrder(**order)

        return order

    def create_order(self, order):
        self.logger.info("Creating order in database")
        db_handler = OrderDatabaseHandler(self.session)
        order_id = db_handler.create_order(order)
        self.logger.info(f"Order created in database: id {order_id}")
        return order_id

    def receive_order(self):
        if order := self.validate_order(self.order):
            order_id = self.create_order(order)
            return 'awaiting_payment', order_id
        else:
            self.logger.info("Order is not valid")
            return 'canceled', None
