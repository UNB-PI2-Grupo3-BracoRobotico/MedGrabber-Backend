import logging
import hashlib

from sqlalchemy import text

from grabber_backend.database_controller.models import User


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class UserDatabaseHandler:
    def __init__(self, db_session):
        self.session = db_session

    def insert_user(self, user: User):
        session = self.session
        status = ""

        try:
            logger.info(f"Inserting user: {user.firebase_uid}")

            session.execute(
                text(
                    "INSERT INTO users (user_id, email, store_name, machine_serial_number, phone_number) "
                    "VALUES (:user_id, :email, :store_name, :machine_serial_number, :phone_number)"
                ),
                {
                    "user_id": user.firebase_uid,
                    "email": user.email,
                    "store_name": user.store_name,
                    "machine_serial_number": user.machine_serial_number,
                    "phone_number": user.phone_number,
                },
            )

            session.commit()

            status = "inserted"

        except Exception as e:
            logger.error(f"Failed to insert user: {user.firebase_uid} - {e}")
            session.rollback()

            status = f"failed - {e}"

            raise e

        return status

    def update_user(self, session, user: User):
        session.execute(
            text(
                "UPDATE users SET email = :email, store_name = :store_name, "
                "personal_name = :personal_name, machine_serial_number = :machine_serial_number, "
                "phone_number = :phone_number, user_role = :user_role WHERE username = :username"
            ),
            {
                "email": user.email,
                "store_name": user.store_name,
                "personal_name": user.personal_name,
                "machine_serial_number": user.machine_serial_number,
                "phone_number": user.phone_number,
                "user_role": user.user_role,
                "username": user.username,
            },
        )
