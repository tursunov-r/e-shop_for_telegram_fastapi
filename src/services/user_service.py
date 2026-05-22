from datetime import timedelta

from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth import create_access_token
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
)
from src.repositories.user_repository import user_repository
from src.utils.exceptions.exceptions import InvalidCredentials


class User:
    @staticmethod
    async def create_user(user: UserCreateSchema, session: AsyncSession):
        create_user = await user_repository.create_user_query(
            user=user, session=session
        )
        return create_user

    @staticmethod
    async def login_user(
        user: UserLoginSchema, response: Response, session: AsyncSession
    ):
        login = await user_repository.login_user_query(
            user=user, session=session
        )
        if not login:
            raise InvalidCredentials("Invalid credentials")
        print(f"logged in {login}")
        # Создание токена
        access_token = create_access_token(
            data={"user_id": login.id, "email": login.email},
            expires_delta=timedelta(),
        )
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600 * 24,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_users(session: AsyncSession):
        users = await user_repository.get_users_query(session=session)
        return users

    @staticmethod
    async def delete_user(user: UserLoginSchema, session: AsyncSession):
        delete_user = await user_repository.delete_user_query(
            user=user, session=session
        )
        if not delete_user:
            raise ValueError("User not found")
        return Response(status_code=204)
