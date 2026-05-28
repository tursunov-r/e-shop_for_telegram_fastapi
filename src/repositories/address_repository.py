from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload


from src.models.address_model import AddressModel
from src.schemas.user_schemas import TokenData, AddressSchema


class AddressRepository:
    @staticmethod
    async def create_address(
        user: TokenData, address: AddressSchema, session: AsyncSession
    ):
        new_address = AddressModel(
            user_id=user.user_id,
            title=address.title,
            first_name=address.first_name,
            last_name=address.last_name,
            phone=address.phone,
            country=address.country,
            city=address.city,
            address=address.address,
        )
        session.add(new_address)
        return new_address


address_repository = AddressRepository()
