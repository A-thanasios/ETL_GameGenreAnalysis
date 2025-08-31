from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, String, false, Engine, select
from sqlalchemy.orm import (
    mapped_column,
    Mapped, Session
)
from sqlalchemy.testing.pickleable import User

from src.db.user_src.base import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_id: Mapped[str] = mapped_column(String(17),unique=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    isPrivate: Mapped[bool] = mapped_column(server_default=false(), nullable=False)
    isExtracted: Mapped[bool] = mapped_column(server_default=false(), nullable=False)

    @staticmethod
    def add_user(engine: Engine, user_id: str):
        with Session(engine) as session:
            user = User(steam_id=user_id)
            session.add(user)
            session.commit()

    @staticmethod
    def add_users(engine: Engine, users_id: list[str]):
        users = []
        for user_id in users_id:
            users.append(User(steam_id=user_id))

        with Session(engine) as session:
            session.add_all(users)
            session.commit()

    @staticmethod
    def get_user(engine: Engine, user_id: str) -> Optional[User]:
        with Session(engine) as session:
            return session.scalars(User.get_single_user_stmt(user_id)).one()

    @staticmethod
    def update_private(engine: Engine, user_id: str, is_private: bool=True):
        User.get_user(engine, user_id).isPrivate = is_private
        with Session(engine) as session:
            session.commit()

    @staticmethod
    def update_extracted(engine: Engine, user_id: str, is_extracted: bool = True):
        User.get_user(engine, user_id).isPrivate = is_extracted
        with Session(engine) as session:
            session.commit()

    @staticmethod
    def delete_user(engine: Engine, user_id: str):
        with Session(engine) as session:
            session.delete(User.get_user(engine, user_id))
            session.commit()


    @staticmethod
    def get_single_user_stmt(user_id):
        return (
            select(User)
            .where(User.steam_id == user_id)
        )

    def __repr__(self) -> str:
        return f"<User(id={self.id},steam_id={self.steam_id}, createdAt={self.createdAt}, updatedAt={self.updatedAt}, isPrivate={self.isPrivate}, isExtracted={self.isExtracted})>"
