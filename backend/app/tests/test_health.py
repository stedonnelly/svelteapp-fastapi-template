import pytest
from app.main import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_healthz():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        r = await ac.get("/api/v1/health/healthz")
        assert r.status_code == 200
        assert r.json()["status"] == "ok"
