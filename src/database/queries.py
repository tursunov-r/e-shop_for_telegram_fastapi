from src.core.db_connect import engine
from src.models.base_model import (
    Base,
)
from src.repositories.user_repository import UserRepository


async def create_tables():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        # await UserRepository.create_admin_query(conn)
