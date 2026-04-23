from collections.abc import AsyncGenerator

import asyncpg
import httpx
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
)
from src.core.settings import settings

engine = create_async_engine(
    url=settings.db_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
)

async_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        async with session.begin():
            yield session


db_pool: asyncpg.Pool | None = None
http_client: httpx.AsyncClient | None = None


async def get_pool():
    global db_pool, http_client
    db_pool = await asyncpg.create_pool(
        settings.pool_url, min_size=10, max_size=20, command_timeout=10
    )
    http_client = httpx.AsyncClient(timeout=5)


async def get_db():
    async with db_pool.acquire() as conn:
        yield conn
