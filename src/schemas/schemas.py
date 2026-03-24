from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int

class UpdateProductSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None