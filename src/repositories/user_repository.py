from fastapi import HTTPException
from sqlalchemy import select

from src.core.db_connect import create_session
from src.models.user_model import UserModel
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
)
from src.utils.auth import hash_password, verify_password


class UserRepository:
    @staticmethod
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

    @staticmethod
    async def login_user_query(user: UserLoginSchema):
        async with create_session() as session:
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
    async def get_users_query():
        async with create_session() as session:
            result = await session.execute(select(UserModel))
            user = result.scalars().all()
            if user:
                return user
            raise HTTPException(status_code=404, detail="User not found")
