from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user_model import UserModel
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
)
from src.utils.auth import hash_password, verify_password


class UserRepository:
    @staticmethod
    async def create_user_query(user: UserCreateSchema, session: AsyncSession):
        email = await session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        result = email.scalar_one_or_none()
        if result:
            raise HTTPException(
                status_code=400, detail="Email already registered"
            )
        hash_pwd = hash_password(user.password)
        query = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=hash_pwd,
            balance=user.balance,
        )
        session.add(query)
        await session.flush()
        await session.refresh(query)
        return query

    @staticmethod
    async def login_user_query(user: UserLoginSchema, session: AsyncSession):
        query = await session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        result = query.scalar_one_or_none()
        if result:
            verified = verify_password(user.password, result.password)
            if verified:
                return True
        raise HTTPException(status_code=401, detail="Invalid credentials")

    @staticmethod
    async def get_users_query(session: AsyncSession):
        result = await session.execute(select(UserModel))
        users = result.scalars().all()
        if users:
            return users
        raise HTTPException(status_code=404, detail="User not found")
