import logging
from sqlalchemy import text, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime
from fastapi import status, HTTPException

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class ProductDatabaseHandler:
    def __init__(self, db_session):
        self.session = db_session

    def get_products(self):
        session = self.session
        try: 
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
                    is_hidden = FALSE
                    AND pos.is_exit = FALSE;
            """
                )
            )
        except Exception as e:
            logger.error(f"Failed to get products with position")
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Failed select products!")
        
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
                "position_y": row[9],
            }
            for row in result_filled_positions
        ]
        return filled_positions

    def insert_product(self, product):
        session = self.session
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
        except Exception as e:
            logger.error(f"Failed to insert product: {product.product_name} - {e}")
            session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product already exist in this position!")
            
        return "product created"
    
    def delete_product(self, product_id, delete_product):
        session = self.session
        try:
            logger.info(f"Deleting product with ID: {product_id}")
            session.execute(
                text(
                    """
                    SELECT delete_product(
                        :product_id,
                        :modified_by
                    )
                    """
                ),
                {
                    "product_id": product_id,
                    "modified_by": delete_product.modified_by_user
                },
            )
            session.commit()
        except Exception as e:
            logger.error(f"Failed to delete product with ID {product_id}: {e}")
            session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Product {product_id} not founded!")
        
        return f"Product {product_id} deleted successfully"


    def update_product(self, product_id, update_product):
        session = self.session
        try:

            session.execute(
                text(
                    """
                    SELECT update_product(
                        :product_id,
                        :product_name,
                        :product_description,
                        :product_price,
                        :peso,
                        :size,
                        :modified_by_user,
                        :position_x,
                        :position_y,
                        :product_amount 
                    )
                    """
                ),
                {
                    "product_id": product_id,
                    "product_name": update_product.product_name,
                    "product_description": update_product.product_description,
                    "product_price": update_product.product_price,
                    "peso": update_product.peso,
                    "size": update_product.size,
                    "modified_by_user": update_product.modified_by_user,
                    "position_x": update_product.position_x,
                    "position_y": update_product.position_y,
                    "product_amount": update_product.amount,
                },
            )
            session.commit()
        except Exception as e:
            logger.error(f"Failed to update product: {product_id} - {e}")
            session.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="product update failed")
        return f"Product {product_id} updated succesfully"
