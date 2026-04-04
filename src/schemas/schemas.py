from pydantic import BaseModel, Field


class CreateProductSchema(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The title of the product.",
    )
    description: str = Field(
        ...,
        min_length=0,
        max_length=100,
        description="The description of the product.",
    )
    price: float = Field(..., ge=1, description="The price of the product.")
    quantity: int = Field(
        ..., ge=0, description="The quantity of the product."
    )


class UpdateProductSchema(BaseModel):
    id: int
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="The title of the product.",
    )
    description: str | None
    price: float
    quantity: int

    class Config:
        from_attributes = True


class ProductItem(BaseModel):
    product_id: int
    quantity: int


class CreateOrderSchema(BaseModel):
    user_id: int
    product_ids: list[ProductItem]

    class Config:
        from_attributes = True


class UpdateOrderSchema(BaseModel):
    order_id: int
    status: str


class UserLoginSchema(BaseModel):
    username: str
    password: str
