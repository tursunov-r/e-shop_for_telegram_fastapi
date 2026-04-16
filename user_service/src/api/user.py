from fastapi import APIRouter, Response, Request

from src.core.limiter import limiter
from user_service.src.services.user_service import User
from user_service.src.schemas.user_schema import (
    UserCreateSchema,
    UserLoginSchema,
    UserCreateResponseSchema,
)

router = APIRouter(prefix="/users/v1", tags=["user"])
user_service = User


@router.post("/create", response_model=UserCreateResponseSchema)
@limiter.limit("5/minute")
async def create_user(user: UserCreateSchema, request: Request):
    await user_service.create_user(user)
    return {"message": "User created successfully"}


@router.post("/login")
@limiter.limit("5/minute")
async def login(user: UserLoginSchema, response: Response, request: Request):
    result = await user_service.login_user(user, response)
    return result


@router.get("/")
@limiter.limit("5/minute")
async def get_users(request: Request):
    users = await user_service.get_users()
    return {"users": users}
