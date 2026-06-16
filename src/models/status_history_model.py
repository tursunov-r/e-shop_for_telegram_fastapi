from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from src.models.base_model import Base


class StatusHistoryModel(Base):
    __tablename__ = "statuses_history"
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    status: Mapped[str] = mapped_column(nullable=False, default="created")
    at: Mapped[datetime] = mapped_column(default=func.now(), nullable=False)
    order = relationship("OrderModel", back_populates="statuses_history")
