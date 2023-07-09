from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class DatabaseHandler:
    def __init__(self, db_uri):
        self.engine = create_engine(db_uri)
        self.session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def create_session(self):
        return self.session()

    def close_session(self, session):
        session.close()

    def add_record(self, session, record):
        session.add(record)
        session.commit()

    def update_record(self, session):
        session.commit()

    def delete_record(self, session, record):
        session.delete(record)
        session.commit()
