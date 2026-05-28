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
