from fastapi import HTTPException, Response

from src.utils.auth import security, config
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
)
from src.repositories.user_repository import UserRepository

user_repo = UserRepository()


class User:
    @staticmethod
    async def create_user(user: UserCreateSchema):
        create_user = await user_repo.create_user_query(user=user)
        return create_user

    @staticmethod
    async def login_user(user: UserLoginSchema, response: Response):
        login = await user_repo.login_user_query(user=user)
        if not login:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}

    @staticmethod
    async def get_users():
        users = await user_repo.get_users_query()
        if users:
            return users
        else:
            return {"message": "No users found"}
