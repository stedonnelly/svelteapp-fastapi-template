from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session
from app.schemas.user import LoginIn, UserOut
from app.services.users import authenticate
from app.auth.session_manager import create_session, set_session_cookie, clear_session_cookie
from app.auth.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/login", response_model=UserOut)
async def login(payload: LoginIn, response: Response, db: AsyncSession = Depends(get_session)):
    user = await authenticate(db, payload.username, payload.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    session_id = await create_session(db, user.id)
    set_session_cookie(response, session_id)
    return UserOut.model_validate(user)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    # We clear cookie; optional enhancement: also delete server session by ID if you decode it.
    clear_session_cookie(response)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get("/me", response_model=UserOut)
async def me(current_user: User = Depends(get_current_user)):
    return UserOut.model_validate(current_user)

