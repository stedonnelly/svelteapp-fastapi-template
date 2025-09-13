from app.models.user import User
from app.utils.security import hash_password, verify_password
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_by_username(db: AsyncSession, username: str) -> User | None:
    q = select(User).where(User.username == username)
    return (await db.execute(q)).scalar_one_or_none()


async def create_user(db: AsyncSession, username: str, password: str, email: str | None) -> User:
    user = User(username=username, password_hash=hash_password(password), email=email)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def authenticate(db: AsyncSession, username: str, password: str) -> User | None:
    user = await get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
