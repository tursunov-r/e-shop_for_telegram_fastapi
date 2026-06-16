from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.services.address_service import address_service
from src.core.db_connect import get_session
from src.schemas.user_schemas import AddressSchema, TokenData
from src.utils.auth import get_current_user

router = APIRouter(prefix="/api/v1/address", tags=["address v1"])


@router.post("/", response_model=AddressSchema, status_code=201)
async def create_address(
    address: AddressSchema,
    session: AsyncSession = Depends(get_session),
    user: TokenData = Depends(get_current_user),
):
    await address_service.create_address(
        address=address, session=session, user=user
    )
    return address
