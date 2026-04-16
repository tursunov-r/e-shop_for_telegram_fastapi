from fastapi import HTTPException, Response

from user_service.src.utils.auth import security, config
from user_service.src.database.queries import (
    create_user_query,
    login_user_query,
    get_users_query,
)
from user_service.src.schemas.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
)


class User:
    @classmethod
    async def create_user(cls, user: UserCreateSchema):
        create_user = await create_user_query(user=user)
        if not create_user:
            raise HTTPException(status_code=404, detail="User already exists")
        return create_user

    @classmethod
    async def login_user(cls, user: UserLoginSchema, response: Response):
        login = await login_user_query(user=user)
        if not login:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        token = security.create_access_token(uid="12345")
        response.set_cookie(config.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}

    @classmethod
    async def get_users(cls):
        users = await get_users_query()
        if users:
            return users
        else:
            return {"message": "No users found"}
