from datetime import datetime
from typing import Optional, Mapping, Any, TypeVar
from enum import Enum

from sqlalchemy import DateTime, func, String, false, select, update
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import (
    mapped_column,
    Mapped, InstrumentedAttribute
)

from src.db.user_src.base import Base

V = TypeVar("V")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    steam_id: Mapped[str] = mapped_column(String(17),unique=True, nullable=False)
    createdAt: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updatedAt: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    extractedAt: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
    isPrivate: Mapped[bool] = mapped_column(server_default=false(), nullable=False)




    @staticmethod
    def select_stmt(user_id: list[str] | None= None,
                    filter_by: Mapping[InstrumentedAttribute, Any] | None=None,
                    ordered_by: Mapping[InstrumentedAttribute, bool] | None=None,
                    limit: int | None=100):
        stmt = select(User)
        if user_id:
            stmt.where(User.steam_id.in_(user_id))
        if filter_by:
            for col, val in filter_by.items():
                stmt = stmt.where(col == val)
        if limit:
            stmt = stmt.limit(limit)
        if ordered_by:
            for col, b_desc in ordered_by.items():
                stmt = stmt.order_by(col.desc() if b_desc else col.asc())

        return stmt

    @staticmethod
    def insert_stmt(user_id: Mapping[InstrumentedAttribute, str]):
        return insert(User).values(user_id).on_conflict_do_nothing(index_elements=[User.steam_id])

    @staticmethod
    def update_stmt(user_id: str | list[str], **kwargs):
        stmt = update(User)
        if not isinstance(user_id, list):
            stmt = stmt.where(User.steam_id == user_id)
        else:
            stmt = stmt.where(User.steam_id.in_(user_id))
        return stmt.values(**kwargs)

    @staticmethod
    def to_attr_mapping(data: Mapping[str, V]|dict[str, V]) -> dict[InstrumentedAttribute, V]:
        """
        Turn {"col_name": value} into {User.col_name: value}, validating that each key
        is a mapped attribute.
        """
        out: dict[InstrumentedAttribute, V] = {}
        for key, value in data.items():
            try:
                attr = getattr(User, key)
            except AttributeError as exc:
                raise KeyError(f"{User.__name__}.{key} does not exist") from exc
            if not isinstance(attr, InstrumentedAttribute):
                raise KeyError(f"{User.__name__}.{key} is not a mapped column")
            out[attr] = value
        return out

    def __repr__(self) -> str:
        return f"<User(id={self.id}, steam_id={self.steam_id}, createdAt={self.createdAt}, updatedAt={self.updatedAt}, isPrivate={self.isPrivate}, isExtracted={self.isExtracted})>"
