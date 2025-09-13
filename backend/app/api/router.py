from app.api.v1 import auth, health, users
from fastapi import APIRouter

api_router = APIRouter(prefix="/api")
api_router.include_router(health.router, prefix="/v1/health", tags=["health"])
api_router.include_router(auth.router, prefix="/v1/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/v1/users", tags=["users"])
