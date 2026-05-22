from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
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

    orders = relationship("OrderModel", back_populates="user")
    address = relationship("AddressModel", back_populates="user")
    role = relationship("RoleModel", back_populates="user")


class AddressModel(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(
        nullable=False, default=UserModel.first_name
    )
    last_name: Mapped[str] = mapped_column(
        nullable=False, default=UserModel.last_name
    )
    phone: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    user = relationship("UserModel", back_populates="address")


class RoleModel(Base):
    __tablename__ = "roles"
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), primary_key=True, index=True
    )
    role: Mapped[str] = mapped_column(nullable=False, default="user")

    user = relationship("UserModel", back_populates="role")
