from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_session

router = APIRouter()

@router.get("/healthz")
async def healthz():
    return {"status": "ok"}

@router.get("/readyz")
async def readyz(db: AsyncSession = Depends(get_session)):
    # Touch DB
    await db.execute("SELECT 1")
    return {"status": "ready"}

