import logging
from sqlalchemy import text, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ProductDatabaseHandler:
    def __init__(self, db_session):
        self.session = db_session

    def get_products(self):
        session = self.session
        status = ""
        result_filled_positions = session.execute(
            text(
                """
            SELECT 
                p.product_id,
                p.product_name,
                p.product_description,
                p.product_price,
                p.peso,
                p.size,
                p.modified_by,
                pos.product_amount,
                pos.position_x,
                pos.position_y
            FROM 
                position pos
            JOIN 
                product p 
            ON 
                pos.product_id = p.product_id
            WHERE 
                pos.is_exit = FALSE;
        """
            )
        )

        filled_positions = [
            {
                "product_id": row[0],
                "product_name": row[1],
                "product_description": row[2],
                "product_price": row[3],
                "peso": row[4],
                "size": row[5],
                "modified_by_user": row[6],
                "amount": row[7],
                "position_x": row[8],
                "position_y": row[9]
            }
            for row in result_filled_positions
        ]
        return filled_positions

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
                    :modified_by_user,
                    :position_x,
                    :position_y,
                    :amount
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
                    SET product_id = NULL,
                        product_amount = 0
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
            session.execute(
                text(
                    """
                    UPDATE position
                    SET product_id = NULL
                    WHERE
                        product_id = :product_id;
                    """
                ),
                {"product_id": product_id},
            )
            if(update_product.amount > 0): 
                session.execute(
                    text("""
                        UPDATE position
                        SET product_id = :product_id,
                            product_amount = :amount,
                            modified_by = :modified_by_user,
                            modified_at = CURRENT_TIMESTAMP
                        WHERE 
                            position_x = :position_x 
                            AND position_y = :position_y 
                            AND is_exit = FALSE; 
                    """),
                    {
                        "product_id": product_id,
                        "amount": update_product.amount,
                        "position_x": update_product.position_x,
                        "position_y": update_product.position_y,
                        "modified_by_user": update_product.modified_by_user
                    }
                )
            
            session.execute(
                text("""
                    UPDATE product
                    SET
                        product_name = :product_name,
                        product_description = :product_description,
                        product_price = :product_price,
                        peso = :peso,
                        size = :size,
                        modified_by = :modified_by_user,
                        modified_at = CURRENT_TIMESTAMP
                    WHERE
                        product_id = :product_id;
                """),
                {
                    "product_id": product_id,
                    "modified_by_user": update_product.modified_by_user,
                    "product_name": update_product.product_name,
                    "product_description": update_product.product_description,
                    "product_price": update_product.product_price,
                    "peso": update_product.peso,
                    "size": update_product.size,
                    "modified_by_user": update_product.modified_by_user
                }
            )
            session.commit()
            status = "updated"

        except Exception as e:
            logger.error(f"Failed to update product: {product_id} - {e}")
            session.rollback()

            status = "failed"

        return status
