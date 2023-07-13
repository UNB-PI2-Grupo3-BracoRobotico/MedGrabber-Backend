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


class StashDatabaseController:
    def __init__(self, session):
        self.session = session

    # Call the stored procedure to create a product
    def create_product(self, product: Product):
        self.session.execute(
            text(
                "SELECT create_product(:product_name, :product_description, :product_price, :modified_by)"
            ),
            {
                "product_name": product.product_name,
                "product_description": product.product_description,
                "product_price": product.product_price,
                "modified_by": product.modified_by,
            },
        )
        self.session.commit()
