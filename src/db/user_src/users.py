from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, func, String, false, Engine
from sqlalchemy.orm import (
    mapped_column,
    Mapped, Session
)

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

    def __repr__(self) -> str:
        return f"<User(id={self.id},steam_id={self.steam_id}, createdAt={self.createdAt}, updatedAt={self.updatedAt}, isPrivate={self.isPrivate}, isExtracted={self.isExtracted})>"
