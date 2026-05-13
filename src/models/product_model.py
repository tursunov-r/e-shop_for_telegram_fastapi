from datetime import datetime
from decimal import Decimal

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.models.base_model import Base


class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(nullable=False, index=True)
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    description: Mapped[str] = mapped_column(nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    order_items = relationship("OrderItemModel", back_populates="product")
