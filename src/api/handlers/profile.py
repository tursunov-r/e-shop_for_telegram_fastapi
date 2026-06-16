from fastapi import APIRouter, Request, Response, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.core.limiter import limiter
from src.schemas.user_schemas import UserLoginSchema, TokenData, UserData
from src.core.db_connect import get_session
from src.services.profile_service import profile_service
from src.services.log_service import log_service
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/profile", tags=["profile v1"])


@router.post("/")
@limiter.limit("5/minute")
async def login(
    user: UserLoginSchema,
    response: Response,
    request: Request,
    session: AsyncSession = Depends(get_session),
):
    result = await profile_service.login_user(
        user=user, response=response, session=session
    )
    log_service.info("user logged in", user=result)
    return result


@router.get("/", response_model=UserData)
@limiter.limit("5/minute")
async def get_profile(
    request: Request,
    session: AsyncSession = Depends(get_session),
    user_token: TokenData = Depends(get_current_user),
):
    profile = await profile_service.get_user_profile(
        session=session, user=user_token
    )
    log_service.info("user profile fetched", profile=profile)
    return profile


@router.post("/logout")
@limiter.limit("5/minute")
async def logout(
    request: Request,
    response: Response,
):
    await profile_service.logout_user(response)

    response.status_code = status.HTTP_204_NO_CONTENT
    return response
