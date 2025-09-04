from typing import Mapping

from sqlalchemy import delete, func
from sqlalchemy.orm import Session, Mapped

from src.db.user_repo import UserRepo
from src.db.user_src.users import User


class UserSrcRepo(UserRepo):
    def create(self, user_id: str|list[str]) -> None:
        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])
        if not ids:
            return

        try:
            with Session(self.engine) as session:
                session.execute(User.insert_stmt(
                    [User.to_attr_mapping({'steam_id': id}) for id in ids]
                ))
                session.commit()
        except Exception as e:
            print(f"Error creating user(s) {ids}: {e}")

    def read(self, user_id: str|list[str]|None=None,
            filter_by: dict[str, bool] | None=None,
            ordered_by: dict[str, bool] | None=None,
            limit: int|None= 100) -> User | list[User] | None:

        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])

        if filter_by:
            filter_by = User.to_attr_mapping(filter_by)

        if ordered_by:
            ordered_by = User.to_attr_mapping(ordered_by)

        with Session(self.engine) as session:
            result = session.scalars(User.select_stmt(ids, filter_by, ordered_by, limit))
            if isinstance(user_id, str):
                return result.one()
            else:
                return list(result.all())

    def update(self, user_id: str | list[str] | Mapped[str], **kwargs) -> None:
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

        try:
            with Session(self.engine) as session:
                session.execute(User.update_stmt(user_ids, **update_kwargs, updatedAt=func.now()))
                session.commit()
        except Exception as e:
            print(f"Error updating user(s) {user_ids}: {e}")


    def delete(self, user_id: str | list[str]):
        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])
        if not ids:
            return

        with Session(self.engine) as session:
            session.execute(delete(User).where(User.steam_id.in_(ids)))
            session.commit()
