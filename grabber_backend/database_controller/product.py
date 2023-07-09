import logging
from sqlalchemy import text, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ProductDatabaseHandler:
    def __init__(self, db_session):
        self.session = db_session

    def insert_product(self, product):
        session = self.session
        status = ""

        try:
            logger.info(f"Inserting product: {product.product_name}")

            session.execute(text("""
                SELECT create_product_and_position(
                    :product_name,
                    :product_description,
                    :product_price,
                    :peso,
                    :size,
                    :modified_by_username,
                    :position_x,
                    :position_y,
                    :product_amount
                );
            """), params=product.dict())

            session.commit()

            status = "inserted"

        except Exception as e:
            logger.error(f"Failed to insert product: {product.product_name} - {e}")
            session.rollback()

            status = "failed"

        return status
