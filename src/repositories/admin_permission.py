from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.schemas.user_schemas import TokenData
from src.models.role_model import RoleModel
from src.utils.exceptions.exceptions import PermissionDeniedError


class AdminPermission:
    @staticmethod
    async def check_permission(
        session: AsyncSession,
        user: TokenData,
    ):
        stmt = select(RoleModel).where(RoleModel.user_id == user.user_id)
        result = await session.execute(stmt)
        role = result.scalar_one_or_none()

        if not role or role.role not in {"admin", "manager", "seller"}:
            raise PermissionDeniedError("No permission")
        return


admin_permission = AdminPermission()
