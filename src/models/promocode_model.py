from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base_model import Base


class PromocodeModel(Base):
    __tablename__ = "promocodes"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    promocode: Mapped[str] = mapped_column(nullable=True)
    orders = relationship("OrderModel", back_populates="promocode")
