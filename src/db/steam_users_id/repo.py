from sqlalchemy import delete, func
from sqlalchemy.orm import Session, Mapped

from db.user_repo import UserRepo
from db.steam_users_id.users import User

class SteamUserRepo(UserRepo):
    def create(self, user_id: str | list[str]):
        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])
        if not ids:
            return

        result = self.execute(User.insert_stmt(
            [User.to_attr_mapping({'steam_id': steam_id}) for steam_id in ids]))
        return result


    def read(self, user_id: str|list[str] | None=None,
            filter_by: dict[str, bool] | None=None,
            ordered_by: dict[str, bool] | None=None,
            limit: int | None= 100) \
            -> User | list[User] | None:

        ids = [user_id] if isinstance(user_id, str) else list(user_id or [])

        if filter_by:
            filter_by = User.to_attr_mapping(filter_by)

        if ordered_by:
            ordered_by = User.to_attr_mapping(ordered_by)

        return self.scalars(User.select_stmt(ids, filter_by, ordered_by, limit))

    def update(self, user_id: str | list[str] | Mapped[str], **kwargs) \
            -> None:
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
        
        self.execute(User.update_stmt(user_ids, **update_kwargs, updatedAt=func.now()))


    def delete(self, user_id: str | list[str]):
        self.execute(User.delete_stmt(user_id))
