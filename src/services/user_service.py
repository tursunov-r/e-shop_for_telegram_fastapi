from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.admin_permission import admin_permission
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    TokenData,
)
from src.repositories.user_repository import user_repository


class UserService:
    @staticmethod
    async def create_user(user: UserCreateSchema, session: AsyncSession):
        create_user = await user_repository.create_user_query(
            user=user, session=session
        )
        return create_user

    @staticmethod
    async def get_users(session: AsyncSession, user: TokenData):
        await admin_permission.check_permission(session, user)
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


user_service = UserService()
