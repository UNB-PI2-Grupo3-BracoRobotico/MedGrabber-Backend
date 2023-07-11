import logging
from sqlalchemy import text, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

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

            session.execute(
                text(
                    """
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
            """
                ),
                params=product.dict(),
            )

            session.commit()

            status = "inserted"

        except Exception as e:
            logger.error(f"Failed to insert product: {product.product_name} - {e}")
            session.rollback()

            status = "failed"

        return status

    def delete_product(self, product_id):
        session = self.session
        status = ""

        try:
            logger.info(f"Deleting product with ID: {product_id}")

            session.execute(
                text(
                    """
                    UPDATE position
                    SET product_id = NULL
                    WHERE product_id = :product_id;
                """
                ),
                {"product_id": product_id},
            )

            session.execute(
                text(
                    """
                    DELETE FROM product WHERE product_id = :product_id;
                """
                ),
                {"product_id": product_id},
            )

            session.commit()

            status = "deleted"

        except Exception as e:
            logger.error(f"Failed to delete product with ID {product_id}: {e}")
            session.rollback()

            status = "failed"

        return status

    def update_product(self, product_id, update_product):
        session = self.session
        status = ""

        try:
            logger.info(f"Updating product: {product_id}")
            update_data = update_product.dict()
            update_data["product_id"] = product_id

            session.execute(
                text(
                    """
                    SELECT update_product_and_position(
                        :product_id,
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
                    """
                ),
                params=update_data,
            )

            session.commit()

            status = "updated"

        except Exception as e:
            logger.error(f"Failed to update product: {product_id} - {e}")
            session.rollback()

            status = "failed"

        return status
