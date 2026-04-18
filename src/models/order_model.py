from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
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
    status: Mapped[str] = mapped_column(nullable=False, default="created")
    total: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    user = relationship("UserModel", back_populates="orders")
    items = relationship("OrderItemModel", back_populates="order")


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
