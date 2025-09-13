from sqlalchemy.orm import DeclarativeBase, declared_attr
from sqlalchemy import text
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(server_default=text("CURRENT_TIMESTAMP"), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        server_default=text("CURRENT_TIMESTAMP"),
        onupdate=text("CURRENT_TIMESTAMP"),
        nullable=False,
    )

@declared_attr
def __tablename__(cls) -> str:  # type: ignore
    return cls.__name__.lower()

