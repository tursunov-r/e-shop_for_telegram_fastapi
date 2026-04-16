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

new_session = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


def create_session() -> AsyncSession:
    return new_session()
