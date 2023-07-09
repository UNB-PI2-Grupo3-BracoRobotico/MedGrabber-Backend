from sqlalchemy.orm import Session
from grabber_backend.database_controller.models import Position


class PositionDatabaseHandler:
    def __init__(self, db_session: Session):
        self.session = db_session

    def insert_position(self, position: Position):
        session = self.session
        status = ""

        try:
            session.add(position)
            session.commit()
            status = "inserted"

        except Exception as e:
            session.rollback()
            status = "failed"
            raise e

        return status

    def update_position(self, position: Position):
        session = self.session
        status = ""

        try:
            session.merge(position)
            session.commit()
            status = "updated"

        except Exception as e:
            session.rollback()
            status = "failed"
            raise e

        return status
