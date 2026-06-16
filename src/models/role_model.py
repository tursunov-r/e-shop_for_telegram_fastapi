from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base_model import Base


class RoleModel(Base):
    __tablename__ = "roles"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )
    role: Mapped[str] = mapped_column(nullable=False, default="user")

    user = relationship("UserModel", back_populates="role")
