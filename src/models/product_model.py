from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
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
    description: Mapped[str] = mapped_column(nullable=False, default="")
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    order_items = relationship("OrderItemModel", back_populates="product")
    translate = relationship("ProductTranslate", back_populates="product")
    image = relationship("ProductImageModel", back_populates="product")


class ProductImageModel(Base):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    path_to_image: Mapped[str] = mapped_column(nullable=False, default="")
    product = relationship("ProductModel", back_populates="images")


class TranslatedProductModel(Base):
    __tablename__ = "translates_products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    lang_code: Mapped[str] = mapped_column(nullable=False, default="ru")
    title: Mapped[str] = mapped_column(nullable=False, default="")
    description: Mapped[str] = mapped_column(nullable=False, default="")
    product = relationship("ProductModel", back_populates="translate")
