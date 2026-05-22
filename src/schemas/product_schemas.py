from typing import List
from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator

from src.utils.barcode_generate import generate_barcode


class CreateProductSchema(BaseModel):
    barcode: str = Field(default=generate_barcode(), description="Barcode")
    price: Decimal = Field(
        ge=0.00,
        max_digits=10_000_000,
        decimal_places=2,
        description="The price of the product.",
    )
    purchase_price: Decimal = Field(
        ge=0.0,
        max_digits=10_000_000,
        decimal_places=2,
        description="The purchase price of the product.",
    )
    stock: int = Field(
        ge=0,
        le=100_000,
        description="The quantity of the product.",
        default=1,
    )

    translate: List["TranslateProductSchema"]
    archived: bool = False


class UpdateProductSchema(BaseModel):
    barcode: str | None = None
    price: Decimal | None = Field(
        default=None,
        ge=0.00,
        max_digits=10_000_000,
        decimal_places=2,
        description="The price of the product.",
    )
    purchase_price: Decimal | None = Field(
        default=None,
        ge=0.0,
        max_digits=10_000_000,
        decimal_places=2,
        description="The purchase price of the product.",
    )
    stock: int | None = Field(
        ge=0,
        le=100_000,
        description="The quantity of the product.",
        default=None,
    )

    translate: List["TranslateProductSchema"] | None = None
    archived: bool | None = None

    class Config:
        from_attributes = True


class SearchProductSchema(BaseModel):
    title: str
    min_price: Decimal = Field(ge=0.00, decimal_places=2)
    max_price: Decimal = Field(ge=0.00, le=10_000_000, decimal_places=2)


class TranslateProductSchema(BaseModel):
    lang_code: str
    title: str
    description: str


class GetProductSchema(BaseModel):
    id: int
    price: Decimal = Field(ge=0.00, decimal_places=2)
    purchase_price: Decimal = Field(ge=0.00, decimal_places=2)
    created_at: datetime
    barcode: str
    quantity: int = Field(ge=0)
    translate: List[TranslateProductSchema]
    archived: bool
