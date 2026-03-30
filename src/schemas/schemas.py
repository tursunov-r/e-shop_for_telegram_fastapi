from pydantic import BaseModel


class CreateProductSchema(BaseModel):
    title: str
    description: str
    price: float
    quantity: int


class UpdateProductSchema(BaseModel):
    id: int
    title: str
    description: str | None
    price: float
    quantity: int

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    title: str | None = None
    description: str | None = None
    price: float | None = None
    quantity: int | None = None


class UserLoginSchema(BaseModel):
    username: str
    password: str
