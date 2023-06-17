import logging

class OrderCreator:
    
    def __init__(self, order):
        self.logger = logging.getLogger(__name__)
        self.db_connection = self.get_db_connection()
        self.order = order
    
    def get_db_connection(self):
        # db_connection = psycopg2.connect(
        #     dbname="grabber",
        #     user="postgres",
        #     password="pass",
        #     host="localhost",
        #     port="5432",
        # )
        # return db_connection
        return True # This is just a fake
    
    def validate_order(self):
        self.logger.info('Validating order')
        pass
    
    def create_order(self):
        self.logger.info('Creating order in database')
        pass
    
    def receive_order(self):
        if self.validate_order():
            self.create_order()
            return True
        