from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class CreateProductSchema(BaseModel):
    title: str = Field(
        min_length=3,
        max_length=100,
        description="The title of the product.",
    )
    description: str = Field(
        min_length=0,
        max_length=100,
        description="The description of the product.",
    )
    price: Decimal = Field(
        ge=0.00,
        max_digits=10_000_000,
        decimal_places=2,
        description="The price of the product.",
    )
    quantity: int = Field(
        ge=0,
        le=100_000,
        description="The quantity of the product.",
    )

    @field_validator("price", mode="before")
    def convert_float(cls, v):
        return Decimal(str(v))


class UpdateProductSchema(BaseModel):
    id: int
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The title of the product.",
    )
    description: str | None
    price: Decimal = Field(
        ge=0.00,
        max_digits=10_000_000,
        decimal_places=2,
        description="The price of the product.",
    )
    quantity: int = Field(
        ge=0,
        le=100_000,
        description="The quantity of the product.",
    )

    @field_validator("price", mode="before")
    def convert_float(cls, v):
        return Decimal(str(v))

    class Config:
        from_attributes = True
