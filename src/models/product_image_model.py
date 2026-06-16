from sqlalchemy import ForeignKey
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)
from src.models.base_model import Base


class ProductImageModel(Base):
    __tablename__ = "product_images"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    path_to_image: Mapped[str] = mapped_column(nullable=True, default="")
    product = relationship("ProductModel", back_populates="images")
