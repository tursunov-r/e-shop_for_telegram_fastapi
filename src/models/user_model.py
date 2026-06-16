from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base_model import Base


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    password: Mapped[str] = mapped_column(nullable=False)
    balance: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    telegram_id: Mapped[int] = mapped_column(
        index=True,
        nullable=True,
        unique=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
    archived: Mapped[bool] = mapped_column(
        nullable=False, default=False, server_default="false"
    )

    orders = relationship("OrderModel", back_populates="user")
    address = relationship("AddressModel", back_populates="user")
    role = relationship("RoleModel", back_populates="user")
