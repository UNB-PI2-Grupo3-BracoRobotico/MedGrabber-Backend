import logging
from sqlalchemy import text, Column, Integer, String, Numeric, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import datetime

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class PositionDatabaseHandler:
    def __init__(self, db_session):
        self.session = db_session

    def get_available_positions(self):
        session = self.session

        try:
            result_empty_positions = session.execute(
                text(
                    """
                SELECT 
                    pos.position_x,
                    pos.position_y
                FROM 
                    position pos
                WHERE 
                    pos.product_id IS NULL AND 
                    pos.is_exit = FALSE;
                """
                )
            )
        except Exception as e:
            raise HTTPException(status_code=409, detail="user update failed")

        available_positions = sorted(
            [
                f"{row[0]}{row[1]}"
                for row in result_empty_positions
                if len(f"{row[0]}{row[1]}") == 2 and f"{row[0]}{row[1]}".isdigit()
            ]
        )
        return available_positions
