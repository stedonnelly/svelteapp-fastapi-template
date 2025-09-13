from app.db.session import get_session
from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

get_session_dep = Depends(get_session)


@router.get("/healthz")
async def healthz():
    return {"status": "ok"}


@router.get("/readyz")
async def readyz(db: AsyncSession = get_session_dep):
    # Touch DB
    await db.execute(text("SELECT 1"))
    return {"status": "ready"}
