import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Response, Request
from itsdangerous import TimestampSigner, BadSignature
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.core.config import settings
from app.models.session import Session

_signer = TimestampSigner(settings.SECRET_KEY)

def _now() -> datetime:
    return datetime.now(timezone.utc)

def make_cookie_value(session_id: str) -> str:
    return _signer.sign(session_id).decode("utf-8")

def read_cookie_value(cookie: str) -> Optional[str]:
    try:
        return _signer.unsign(cookie, max_age=settings.SESSION_MAX_AGE_SECONDS).decode("utf-8")
    except BadSignature:
        return None

async def create_session(db: AsyncSession, user_id: int) -> str:
    session_id = secrets.token_urlsafe(32)
    expires_at = _now() + timedelta(seconds=settings.SESSION_MAX_AGE_SECONDS)
    db.add(Session(session_id=session_id, user_id=user_id, expires_at=expires_at))
    await db.commit()
    return session_id

async def destroy_session(db: AsyncSession, session_id: str) -> None:
    await db.execute(delete(Session).where(Session.session_id == session_id))
    await db.commit()

async def get_user_id_from_request(db: AsyncSession, request: Request) -> Optional[int]:
    cookie = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not cookie:
        return None
    raw = read_cookie_value(cookie)
    if not raw:
        return None
    stmt = select(Session.user_id, Session.expires_at).where(Session.session_id == raw)
    row = (await db.execute(stmt)).first()
    if not row:
        return None
    user_id, expires_at = row
    if expires_at <= _now():
        # Session expired; clean up
        await destroy_session(db, raw)
        return None
    return user_id

def set_session_cookie(response: Response, session_id: str) -> None:
    value = make_cookie_value(session_id)
    response.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=value,
        max_age=settings.SESSION_MAX_AGE_SECONDS,
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax" if not settings.SECURE_COOKIES else "strict",
        path="/",
    )

def clear_session_cookie(response: Response) -> None:
    response.delete_cookie(
        key=settings.SESSION_COOKIE_NAME,
        path="/",
        httponly=True,
        secure=settings.SECURE_COOKIES,
        samesite="lax" if not settings.SECURE_COOKIES else "strict",
    )

