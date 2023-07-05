import logging
from sqlalchemy import text, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Product:
    def __init__(self, product_id, product_name, product_description, product_price, modified_by_username, modified_at):
        self.product_id = product_id
        self.product_name = product_name
        self.product_description = product_description
        self.product_price = product_price
        self.modified_by_username = modified_by_username
        self.modified_at = modified_at

class ProductDatabaseHandler:
    def __init__(self, db_session):
        self.session = db_session

    def insert_product(self, product: Product):
        session = self.session
        status = ""

        try:
            logger.info(f"Inserting product: {product.product_name}")

            session.execute(
                text(
                    "INSERT INTO products (product_id, product_name, product_description, product_price, modified_by_username, modified_at) "
                    "VALUES (:product_id, :product_name, :product_description, :product_price, :modified_by_username, :modified_at)"
                ),
                {
                    "product_id": product.product_id,
                    "product_name": product.product_name,
                    "product_description": product.product_description,
                    "product_price": product.product_price,
                    "modified_by_username": product.modified_by_username,
                    "modified_at": product.modified_at,
                },
            )

            session.commit()

            status = "inserted"

        except Exception as e:
            logger.error(f"Failed to insert product: {product.product_name} - {e}")
            session.rollback()

            status = "failed"

        return status

    def update_product(self, product: Product):
        session = self.session

        try:
            session.execute(
                text(
                    "UPDATE products SET product_name = :product_name, product_description = :product_description, "
                    "product_price = :product_price, modified_by_username = :modified_by_username, modified_at = :modified_at "
                    "WHERE product_id = :product_id"
                ),
                {
                    "product_name": product.product_name,
                    "product_description": product.product_description,
                    "product_price": product.product_price,
                    "modified_by_username": product.modified_by_username,
                    "modified_at": product.modified_at,
                    "product_id": product.product_id,
                },
            )

            session.commit()

            return True

        except Exception as e:
            logger.error(f"Failed to update product: {product.product_name} - {e}")
            session.rollback()

            return False
