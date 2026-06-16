from datetime import timedelta
from fastapi import Response
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import UserLoginSchema, TokenData
from src.repositories.user_repository import user_repository
from src.utils.exceptions.exceptions import InvalidCredentials
from src.utils.auth import create_access_token
from src.core.settings import settings


class ProfileService:
    @staticmethod
    async def login_user(
        user: UserLoginSchema, response: Response, session: AsyncSession
    ):
        login = await user_repository.login_user_query(
            user=user, session=session
        )
        if not login:
            raise InvalidCredentials("Invalid credentials")
        # Создание токена
        access_token = create_access_token(
            data={"user_id": login.id, "email": login.email},
            expires_delta=timedelta(),
        )
        response.set_cookie(
            key=settings.JWT_ACCESS_COOKIE_NAME,
            value=access_token,
            httponly=True,
            secure=False,
            samesite="Lax",
            max_age=3600 * 24,
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @staticmethod
    async def get_user_profile(user: TokenData, session: AsyncSession):
        result = await user_repository.get_profile_query(
            user=user, session=session
        )
        return result

    @staticmethod
    async def logout_user(response: Response):
        response.delete_cookie(
            key=settings.JWT_ACCESS_COOKIE_NAME,
            httponly=True,
            secure=False,
            samesite="Lax",
        )


profile_service = ProfileService()
