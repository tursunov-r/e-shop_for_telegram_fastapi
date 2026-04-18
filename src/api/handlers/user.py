from typing import List

from fastapi import APIRouter, Response, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_connect import get_session
from src.core.limiter import limiter
from src.services.user_service import User
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserCreateResponseSchema,
    UserData,
)

router = APIRouter(prefix="/users/v1", tags=["user"])
user_service = User


@router.post("/create", response_model=UserCreateResponseSchema)
@limiter.limit("5/minute")
async def create_user(
    user: UserCreateSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    new_user = await user_service.create_user(user=user, session=session)
    return {"message": "Created", "data": new_user}


@router.post("/login")
@limiter.limit("5/minute")
async def login(
    user: UserLoginSchema,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    result = await user_service.login_user(
        user=user, response=response, session=session
    )
    return result


@router.get("/", response_model=List[UserData])
@limiter.limit("5/minute")
async def get_users(
    request: Request, session: AsyncSession = Depends(get_session)
):
    users = await user_service.get_users(session=session)
    return users
