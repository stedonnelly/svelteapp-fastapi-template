from datetime import datetime
from typing import Any

from sqlalchemy import text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    def __init_subclass__(cls, /, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # generate __tablename__ when subclass doesn't define one explicitly
        if "__tablename__" not in cls.__dict__:
            cls.__tablename__ = cls.__name__.lower()


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )
