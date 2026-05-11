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
        default=1,
    )

    @field_validator("price", mode="before")
    def convert_float(cls, v):
        return Decimal(str(v))


class UpdateProductSchema(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=3,
        max_length=100,
        description="The title of the product.",
    )
    description: str | None = None
    price: Decimal | None = Field(
        default=None,
        ge=0.00,
        max_digits=10_000_000,
        decimal_places=2,
        description="The price of the product.",
    )
    quantity: int | None = Field(
        default=None,
        ge=0,
        le=100_000,
        description="The quantity of the product.",
    )

    @field_validator("price", mode="before")
    def convert_float(cls, v):
        return Decimal(str(v))

    class Config:
        from_attributes = True


class SearchProductSchema(BaseModel):
    title: str
    min_price: Decimal = Field(ge=0.00, decimal_places=2)
    max_price: Decimal = Field(ge=0.00, le=10_000_000, decimal_places=2)


class GetProductSchema(BaseModel):
    id: int
    title: str
    price: Decimal = Field(ge=0.00, decimal_places=2)
    quantity: int = Field(ge=0)
    description: str | None
