from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user import UserCreate, UserOut
from app.services.users import create_user, get_by_username

router = APIRouter()

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(payload: UserCreate, db: AsyncSession = Depends(get_session)):
    existing = await get_by_username(db, payload.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already taken")
    user = await create_user(db, payload.username, payload.password, payload.email)
    return UserOut.model_validate(user)

