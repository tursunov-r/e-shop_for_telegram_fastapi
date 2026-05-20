from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.utils.auth import security, config
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
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}

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
