from abc import ABC, abstractmethod

from src.db.database_factory import Database


class UserRepo(ABC):
    def __init__(self, db: Database):
        if not db:
            raise ValueError("Database is not initialized.")
        if not isinstance(db, Database):
            raise ValueError("Database is not an instance of Database.")
        self.__db = db

    @abstractmethod
    def create(self, user_id: str|list[str]):
        pass

    @abstractmethod
    def read(self, user_id: str|list[str], **kwargs):
        pass

    @abstractmethod
    def update(self, user_id: str):
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass

    @property
    def db(self) -> Database:
        return self.__db

    @property
    def engine(self) -> Database.engine:
        return self.__db.engine