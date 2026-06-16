from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.models.base_model import Base


class TranslatedProductModel(Base):
    __tablename__ = "translates_products"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    lang_code: Mapped[str] = mapped_column(nullable=False, default="ru")
    title: Mapped[str] = mapped_column(nullable=False, default="")
    description: Mapped[str] = mapped_column(nullable=False, default="")
    product = relationship("ProductModel", back_populates="translate")
