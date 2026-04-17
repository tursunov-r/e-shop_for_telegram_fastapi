from pydantic import BaseModel


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
