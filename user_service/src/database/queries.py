from fastapi import HTTPException
from sqlalchemy import select

from src.core.db_connect import create_session
from src.database.models import UserModel
from user_service.src.schemas.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
)
from user_service.src.utils.auth import hash_password, verify_password


async def create_user_query(user: UserCreateSchema):
    async with create_session() as session:
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
        await session.commit()
        return query


async def login_user_query(user: UserLoginSchema):
    async with create_session() as session:
        try:
            query = await session.execute(
                select(UserModel).where(UserModel.email == user.email)
            )
            result = query.scalar_one_or_none()
            verified = verify_password(user.password, result.password)
            if verified:
                return True
            raise HTTPException(status_code=401, detail="Invalid credentials")
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid credentials")


async def get_users_query():
    async with create_session() as session:
        try:
            result = await session.execute(select(UserModel))
            return result.scalars().all()
        except:
            return None
