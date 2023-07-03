from sqlalchemy import create_engine, text

from grabber_backend.database_controller.models import (
    Base,
    User,
    Product,
    Order,
    OrderProduct,
    Payment,
    Position,
    UserRoleEnum,
    OrderStatusEnum,
    PaymentStatusEnum,
)


class UserDatabaseController:
    def __init__(self, session):
        self.session = session

    def create_user(self, user: User):
        self.session.execute(
            text(
                "SELECT create_user(:username, :password_hash, :email, :store_name, :personal_name, :machine_serial_number, :phone_number, :user_role)"
            ),
            {
                "username": user.username,
                "password_hash": user.password_hash,
                "email": user.email,
                "store_name": user.store_name,
                "personal_name": user.personal_name,
                "machine_serial_number": user.machine_serial_number,
                "phone_number": user.phone_number,
                "user_role": user.user_role,
            },
        )
        self.session.commit()
