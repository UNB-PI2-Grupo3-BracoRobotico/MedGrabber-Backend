from database_handler import DatabaseHandler
from user import User

class UserDatabaseHandler:
    def __init__(self, db_handler: DatabaseHandler):
        self.db_handler = db_handler

    def upsert_user(self, user: User):
        session = self.db_handler.create_session()

        try:
            # Chamar a stored procedure correspondente para inserir ou atualizar o usuário
            if user.username:  # Se o username já existir, atualizar o usuário
                self.update_user(session, user)
            else:  # Caso contrário, inserir um novo usuário
                self.insert_user(session, user)
                
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            self.db_handler.close_session(session)

    def insert_user(self, session, user: User):
        # Lógica para mapear os campos do objeto User para os parâmetros da stored procedure
        # e executar a inserção do usuário
        session.execute(
            "INSERT INTO users (username, password_hash, email, store_name, personal_name, machine_serial_number, phone_number, user_role) "
            "VALUES (:username, :password_hash, :email, :store_name, :personal_name, :machine_serial_number, :phone_number, :user_role)",
            {
                "username": user.username,
                "password_hash": user.password_hash,
                "email": user.email,
                "store_name": user.store_name,
                "personal_name": user.personal_name,
                "machine_serial_number": user.machine_serial_number,
                "phone_number": user.phone_number,
                "user_role": user.user_role,
            }
        )

    def update_user(self, session, user: User):
        # Lógica para mapear os campos do objeto User para os parâmetros da stored procedure
        # e executar a atualização do usuário
        session.execute(
            "UPDATE users SET password_hash = :password_hash, email = :email, store_name = :store_name, "
            "personal_name = :personal_name, machine_serial_number = :machine_serial_number, "
            "phone_number = :phone_number, user_role = :user_role WHERE username = :username",
            {
                "password_hash": user.password_hash,
                "email": user.email,
                "store_name": user.store_name,
                "personal_name": user.personal_name,
                "machine_serial_number": user.machine_serial_number,
                "phone_number": user.phone_number,
                "user_role": user.user_role,
                "username": user.username,
            }
        )
