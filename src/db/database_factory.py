from contextlib import contextmanager
import os
from typing import Generator
from enum import Enum

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

class DBType(Enum):
    Steam_user = 'Steam_user'

class Database:
    def __init__(self, engine, session_maker: sessionmaker):
        self._engine = engine
        self._session_maker = session_maker

    @property
    def engine(self):
        return self._engine

    
    @contextmanager
    def session_scope(self) -> Generator[Session, None, None]:
        session = self._session_maker()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()


class DatabaseFactory():
    @staticmethod
    def init_db(db_usage: DBType | str) -> Database|None:
        if db_usage == DBType.Steam_user:
            url = os.getenv('SQLALCHEMY_URL')
            if not url: return None
            
            engine = create_engine(url)
            session_maker = sessionmaker(bind=engine, expire_on_commit=False)
            
            return Database(engine, session_maker)

        elif db_usage == 'test':
            url = os.getenv('SQLALCHEMY_URL_DEV')
            if not url: return None

            engine = create_engine(url)
            session_maker = sessionmaker(bind=engine, expire_on_commit=False)

            return Database(engine, session_maker)
        else:
            raise ValueError("Invalid database usage.")