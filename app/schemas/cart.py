from pydantic import BaseModel
from app.schemas.product import ProductRead

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemRead(BaseModel):
    id: int
    quantity: int
    product: ProductRead

    class Config:
        from_attributes=True


class CartRead(BaseModel):
    id: int
    items: list[CartItemRead]

    class Config:
        from_attributes = True

        