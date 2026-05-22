from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base_model import Base


class OrderModel(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    address_id: Mapped[int] = mapped_column(nullable=False, server_default="0")
    promocode_id: Mapped[int] = mapped_column(
        ForeignKey("promocodes.id"), nullable=True
    )
    total: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(), nullable=False
    )

    user = relationship("UserModel", back_populates="orders")
    items = relationship("OrderItemModel", back_populates="order")
    promocode = relationship("PromocodeModel", back_populates="orders")
    statuses_history = relationship(
        "StatusHistoryModel", back_populates="order"
    )


class OrderItemModel(Base):
    __tablename__ = "order_items"
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"), primary_key=True, index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"), primary_key=True, index=True
    )
    quantity: Mapped[int] = mapped_column(nullable=False, default=1)
    total: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    order = relationship("OrderModel", back_populates="items")
    product = relationship("ProductModel", back_populates="order_items")


class StatusHistoryModel(Base):
    __tablename__ = "statuses_history"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    status: Mapped[str] = mapped_column(nullable=False, default="created")
    at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    order = relationship("OrderModel", back_populates="statuses_history")


class PromocodeModel(Base):
    __tablename__ = "promocodes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    promocode: Mapped[str] = mapped_column(nullable=True)
    orders = relationship("OrderModel", back_populates="promocode")
