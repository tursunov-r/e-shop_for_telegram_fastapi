from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    __abstract__ = True


class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    balance: Mapped[Decimal] = mapped_column(nullable=False, default=0)
    created_at: Mapped[datetime] = mapped_column(
        nullable=False, default=datetime.now
    )

    orders = relationship("OrderModel", back_populates="user")


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
    products = relationship(
        "ProductModel", secondary="order_items", back_populates="orders"
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

    orders = relationship(
        "OrderModel", secondary="order_items", back_populates="products"
    )
