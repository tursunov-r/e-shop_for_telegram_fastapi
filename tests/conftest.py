import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from asgi_lifespan import LifespanManager
from src.api.main import app


@pytest_asyncio.fixture
async def client():
    async with LifespanManager(app):  # 🔥 ВАЖНО
        transport = ASGITransport(app=app)

        async with AsyncClient(
            transport=transport, base_url="http://test"
        ) as ac:
            yield ac


@pytest_asyncio.fixture
def auth_cookie():
    # фейковая кука (если проверка отключена — прокатит)
    return {"access_token": "testtoken"}
