from os import environ as env

DATABASE_CONNECTION = {
    "dbname": env.get("DB_NAME", "grabber"),
    "user": env.get("DB_USER", "postgres"),
    "password": env.get("DB_PASSWORD", "pass"),
    "host": env.get("DB_HOST", "localhost"),
    "port": env.get("DB_PORT", "5432"),
}

DATABASE_CONNECTION_STRING = (
    f"postgresql://"
    f'{DATABASE_CONNECTION["user"]}:{DATABASE_CONNECTION["password"]}'
    f'@{DATABASE_CONNECTION["host"]}:{DATABASE_CONNECTION["port"]}'
    f'/{DATABASE_CONNECTION["dbname"]}'
)
