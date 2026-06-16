from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.user_schemas import TokenData, AddressSchema

from src.repositories.address_repository import address_repository


class AddressService:
    @staticmethod
    async def create_address(
        user: TokenData, address: AddressSchema, session: AsyncSession
    ):
        result = await address_repository.create_address(
            user=user, address=address, session=session
        )
        return result


address_service = AddressService()
