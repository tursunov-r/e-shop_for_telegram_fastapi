from pydantic import BaseModel


class ProductSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int