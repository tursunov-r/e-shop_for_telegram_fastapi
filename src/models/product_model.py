from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.models.base_model import Base


class ProductModel(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    barcode: Mapped[str] = mapped_column(
        nullable=False, index=True, server_default=""
    )
    quantity: Mapped[int] = mapped_column(nullable=False, default=0)
    price: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    purchase_price: Mapped[Decimal] = mapped_column(
        nullable=False, default=0, server_default="0"
    )
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=func.now()
    )
    archived: Mapped[bool] = mapped_column(
        default=False, server_default="false"
    )

    order_items = relationship("OrderItemModel", back_populates="product")
    translate = relationship(
        "TranslatedProductModel",
        back_populates="product",
        cascade="all, delete-orphan",
    )
    image = relationship("ProductImageModel", back_populates="product")


class ProductImageModel(Base):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    path_to_image: Mapped[str] = mapped_column(nullable=True, default="")
    product = relationship("ProductModel", back_populates="image")


class TranslatedProductModel(Base):
    __tablename__ = "translates_products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    lang_code: Mapped[str] = mapped_column(nullable=False, default="ru")
    title: Mapped[str] = mapped_column(nullable=False, default="")
    description: Mapped[str] = mapped_column(nullable=False, default="")
    product = relationship("ProductModel", back_populates="translate")
