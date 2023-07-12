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

    def update_user(self, user_id, user):
        session = self.session
        status = ""
        try:
            update_fields = {}

            if user.email:
                update_fields["email"] = user.email
            if user.store_name:
                update_fields["store_name"] = user.store_name
            if user.machine_serial_number:
                update_fields["machine_serial_number"] = user.machine_serial_number
            if user.phone_number:
                update_fields["phone_number"] = user.phone_number

            if not update_fields:
                raise HTTPException(status_code=400, detail="No fields provided for update")

            session.execute(
                text(
                    """
                    UPDATE users 
                        SET 
                            email = COALESCE(:email, email), 
                            store_name = COALESCE(:store_name, store_name), 
                            machine_serial_number = COALESCE(:machine_serial_number, machine_serial_number), 
                            phone_number = COALESCE(:phone_number, phone_number) 
                        WHERE 
                            user_id = :user_id
                    """
                ),
                {
                    "email": update_fields.get("email"),
                    "store_name": update_fields.get("store_name"),
                    "machine_serial_number": update_fields.get("machine_serial_number"),
                    "phone_number": update_fields.get("phone_number"),
                    "user_id": user_id
                },
            )

            session.commit()
            status = "updated"

        except Exception as e:
            logger.error(f"Failed to update user: {user_id} - {e}")
            session.rollback()
            status = "failed"
            raise HTTPException(status_code=500, detail=f"Failed to update user: {user_id}")

        return status