import os
from dotenv import load_dotenv
from enum import Enum

from sqlalchemy import create_engine


class DBType(Enum):
    USER_SRC = 'USER_SRC'

class Database:
    def __init__(self, engine):
        self.__engine = engine

    @property
    def engine(self):
        return self.__engine


class DatabaseFactory():
    def __init__(self):
        load_dotenv()

    @staticmethod
    def init_db(db_usage: DBType) -> Database:
        if db_usage == DBType.USER_SRC:
            return Database(create_engine(os.getenv('SQLALCHEMY_URL')))
        else:
            raise ValueError("Invalid database usage.")

