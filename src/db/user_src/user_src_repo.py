from typing import Mapping, Any

from sqlalchemy import delete, func
from sqlalchemy.orm import Session, InstrumentedAttribute

from src.db.database_factory import Database
from src.db.user_repo import UserRepo
from src.db.user_src.users import User


class UserSrcRepo(UserRepo):
    def create(self, user_id: str|list[str]) -> None:
        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])
        if not ids:
            return

        users = []
        for item in ids:
            users.append(User(steam_id=item))

        with Session(self.engine) as session:
            session.add_all(users)
            session.commit()

    def read(self, user_id: str|list[str]|None=None,
            filter_by: Mapping[InstrumentedAttribute, Any] | None=None,
            ordered_by: Mapping[InstrumentedAttribute, bool] | None=None,
            limit: int|None= 100) -> User | list[User] | None:

        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])

        with Session(self.engine) as session:
            result = session.scalars(User.select_stmt(ids, filter_by, ordered_by))
            if isinstance(user_id, str):
                return result.one()
            else:
                return list(result.all())

    def update(self, user_id: str | list[str], **kwargs) -> None:
        user_ids = [user_id] if isinstance(user_id, str) else list(user_id or [])
        if not user_ids or not kwargs:
            return

        update_kwargs: dict = {}
        if 'is_private' in kwargs:
            update_kwargs['isPrivate'] = kwargs['is_private']
        if 'is_extracted' in kwargs:
            update_kwargs['isExtracted'] = kwargs['is_extracted']

        if not update_kwargs:
            return

        with Session(self.engine) as session:
            session.execute(User.update_stmt(user_ids, **update_kwargs, updatedAt=func.now()))
            session.commit()


    def delete(self, user_id: str | list[str]):
        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])
        if not ids:
            return

        with Session(self.engine) as session:
            session.execute(delete(User).where(User.steam_id.in_(ids)))
            session.commit()
