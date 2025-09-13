import pytest
from app.core.config import settings
from app.main import app
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_login_me_logout():
    # This test assumes a running DB; in CI use a test DB or mocked layer.
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create user
        r = await ac.post(
            "/api/v1/users/", json={"username": "alice", "password": "passw0rd", "email": None}
        )
        assert r.status_code in (201, 400)  # allow rerun if user already exists

        # Login
        r = await ac.post("/api/v1/auth/login", json={"username": "alice", "password": "passw0rd"})
        assert r.status_code == 200
        assert settings.SESSION_COOKIE_NAME in r.cookies

        # Me
        cookie = {settings.SESSION_COOKIE_NAME: r.cookies[settings.SESSION_COOKIE_NAME]}
        r2 = await ac.get("/api/v1/auth/me", cookies=cookie)
        assert r2.status_code == 200
        assert r2.json()["username"] == "alice"

        # Logout
        r3 = await ac.post("/api/v1/auth/logout", cookies=cookie)
        assert r3.status_code == 204
