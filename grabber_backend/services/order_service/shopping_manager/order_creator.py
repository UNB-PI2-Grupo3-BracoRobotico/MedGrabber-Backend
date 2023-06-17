import logging


class OrderCreator:
    def __init__(self, order):
        self.logger = logging.getLogger(__name__)
        self.db_connection = self.get_db_connection()
        self.order = self.validate_order(order)

    def get_db_connection(self):
        # TODO: use the database_controller package
        return True  # This is just a fake

    def validate_order(self):
        self.logger.info("Validating order")

        pass

    def create_order(self):
        self.logger.info("Creating order in database")
        pass

    def receive_order(self):
        if self.order:
            order_data = self.create_order()
            return order_data
        else:
            self.logger.info("Order is not valid")
            return None
