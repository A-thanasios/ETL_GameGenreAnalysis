from abc import ABC, abstractmethod

from db.database_factory import Database


class UserRepo(ABC):
    def __init__(self, db: Database):
        if not db:
            raise ValueError("Database is not initialized.")
        if not isinstance(db, Database):
            raise ValueError("Database is not an instance of Database.")
        self._db = db

    @abstractmethod
    def create(self, user_id: str|list[str]):
        pass

    @abstractmethod
    def read(self, user_id: str|list[str], ordered_by=None, **kwargs):
        pass

    @abstractmethod
    def update(self, user_id: str):
        pass

    @abstractmethod
    def delete(self, user_id: str):
        pass

    @property
    def db(self) -> Database:
        return self._db

    @property
    def engine(self) -> Database.engine:
        return self._db.engine
    
    @property
    def session_scope(self):
        return self._db.session_scope()
    
    def execute(self, stmt):
        with self.session_scope as session:
            return session.execute(stmt)
    
    def scalars(self, stmt):
        with self.session_scope as session:
            result = session.scalars(stmt)
            users = result.all()
            if users.count == 1:
                return users[0]
            else:
                return users