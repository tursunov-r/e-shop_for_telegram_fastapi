from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base_model import Base


class AddressModel(Base):
    __tablename__ = "addresses"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    title: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[str] = mapped_column(
        nullable=False, default="users.first_name"
    )
    last_name: Mapped[str] = mapped_column(
        nullable=False, default="users.last_name"
    )
    phone: Mapped[str] = mapped_column(nullable=False)
    country: Mapped[str] = mapped_column(nullable=False)
    city: Mapped[str] = mapped_column(nullable=False)
    postal_code: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    user = relationship("UserModel", back_populates="address")
