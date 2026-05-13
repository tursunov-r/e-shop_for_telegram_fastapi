from typing import List

from fastapi import (
    APIRouter,
    Response,
    Request,
    Depends,
    HTTPException,
)
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.db_connect import get_session
from src.core.limiter import limiter
from src.services.log_service import log_service
from src.services.user_service import User
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    UserCreateResponseSchema,
    UserData,
)
from src.utils.statuses import get_status_code

router = APIRouter(prefix="/api/v1/users", tags=["user"])
user_service = User


@router.post("/", response_model=UserCreateResponseSchema)
@limiter.limit("5/minute")
async def create_user(
    user: UserCreateSchema,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    try:
        new_user = await user_service.create_user(user=user, session=session)
        log_service.info("user created", user=new_user)
        return {"message": "Created", "data": new_user}
    except Exception as e:
        log_service.error(
            "error creating user", code=get_status_code(e), exception=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.post("/login")
@limiter.limit("5/minute")
async def login(
    user: UserLoginSchema,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await user_service.login_user(
            user=user, response=response, session=session
        )
        log_service.info("user logged in", user=result)
        return result
    except Exception as e:
        log_service.error(
            "error logging in", code=get_status_code(e), exception=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.get("/", response_model=List[UserData])
@limiter.limit("5/minute")
async def get_users(
    request: Request, session: AsyncSession = Depends(get_session)
):
    try:
        users = await user_service.get_users(session=session)
        log_service.info("users fetched", users=users)
        return users
    except Exception as e:
        log_service.error(
            "error getting users", code=get_status_code(e), exception=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))


@router.delete("/", response_model=UserData)
@limiter.limit("5/minute")
async def delete_user(
    request: Request,
    user: UserLoginSchema,
    session: AsyncSession = Depends(get_session),
):
    try:
        result = await user_service.delete_user(user=user, session=session)
        log_service.info("user deleted", user=result)
        return result
    except Exception as e:
        log_service.error(
            "error deleting user", code=get_status_code(e), exception=str(e)
        )
        raise HTTPException(status_code=get_status_code(e), detail=str(e))
