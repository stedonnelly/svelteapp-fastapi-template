from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.router import api_router

try:
    import orjson
    def orjson_dumps(v, *, default):
        return orjson.dumps(v, default=default).decode()
    json_response_class = None
except Exception:
    orjson = None
    orjson_dumps = None
    json_response_class = None

app = FastAPI(
    title=settings.PROJECT_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

