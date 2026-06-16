from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.settings import settings
from src.models.role_model import RoleModel
from src.models.user_model import UserModel
from src.schemas.user_schemas import (
    UserCreateSchema,
    UserLoginSchema,
    TokenData,
)
from src.utils.auth import hash_password, verify_password
from src.utils.exceptions.exceptions import (
    EmailAlreadyExists,
    InvalidCredentials,
    UserNotFound,
    NotAuthorized,
)


class UserRepository:
    @staticmethod
    async def create_user_query(user: UserCreateSchema, session: AsyncSession):
        email = await session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        result = email.scalar_one_or_none()
        if result:
            raise EmailAlreadyExists("email already exists")
        hash_pwd = hash_password(user.password)
        query = UserModel(
            first_name=user.first_name,
            last_name=user.last_name,
            email=str(user.email),
            password=hash_pwd,
            balance=user.balance,
        )
        session.add(query)
        await session.flush()
        await session.refresh(query)
        return query

    @staticmethod
    async def login_user_query(user: UserLoginSchema, session: AsyncSession):
        query = await session.execute(
            select(UserModel).where(
                and_(
                    UserModel.email == user.email,
                    UserModel.archived.is_(False),
                )
            )
        )
        result = query.scalar_one_or_none()
        if result:
            verified = verify_password(user.password, result.password)
            if verified:
                return result
        raise InvalidCredentials()

    @staticmethod
    async def get_users_query(session: AsyncSession):
        result = await session.execute(
            select(UserModel).options(selectinload(UserModel.address))
        )
        users = result.scalars().all()
        if users:
            return users
        raise UserNotFound("Users not found")

    @staticmethod
    async def get_profile_query(session: AsyncSession, user: TokenData):
        result = await session.execute(
            select(UserModel)
            .options(selectinload(UserModel.address))
            .where(
                and_(
                    UserModel.id == user.user_id, UserModel.email == user.email
                )
            )
        )
        user = result.scalar_one_or_none()
        if user:
            return user
        raise NotAuthorized("User not found")

    @staticmethod
    async def delete_user_query(user: UserLoginSchema, session: AsyncSession):
        result = await session.execute(
            select(UserModel).where(UserModel.email == user.email)
        )
        db_user = result.scalar_one_or_none()
        if not db_user:
            raise UserNotFound("User not found")
        delete_user = UserModel(archived=True)
        session.add(delete_user)
        return db_user

    @staticmethod
    async def create_admin_query(session: AsyncSession):
        hash_pwd = hash_password(settings.admin_password)

        result = await session.execute(
            select(UserModel).where(UserModel.email == settings.admin_email)
        )
        existing = result.scalar_one_or_none()

        if existing:
            return

        create_admin = UserModel(
            email=settings.admin_email,
            password=hash_pwd,
            first_name=settings.admin_first_name,
            last_name=settings.admin_last_name,
        )

        session.add(create_admin)
        await session.flush()

        role = RoleModel(user_id=create_admin.id, role="admin")

        session.add(role)
        await session.commit()


user_repository = UserRepository()
