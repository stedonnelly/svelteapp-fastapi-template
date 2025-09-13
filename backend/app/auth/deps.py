from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_session
from app.auth.session_manager import get_user_id_from_request
from app.models.user import User

async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_session),
) -> User:
    user_id = await get_user_id_from_request(db, request)
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    row = await db.execute(select(User).where(User.id == user_id))
    user = row.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    return user

