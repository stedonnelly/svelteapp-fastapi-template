from datetime import datetime

from app.models.base import Base, TimestampMixin
from sqlalchemy import ForeignKey, Index, Integer, String
from sqlalchemy.orm import Mapped, mapped_column


class Session(Base, TimestampMixin):
    __tablename__ = "sessions"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[str] = mapped_column(String(128), unique=True, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    expires_at: Mapped[datetime] = mapped_column(index=True)


Index("ix_sessions_user_expires", Session.user_id, Session.expires_at)
