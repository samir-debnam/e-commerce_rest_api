from pydantic import BaseModel
from pydantic import ConfigDict
from app.schemas.product import ProductRead

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemRead(BaseModel):
    id: int
    quantity: int
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)


class CartRead(BaseModel):
    id: int
    items: list[CartItemRead]

    model_config = ConfigDict(from_attributes=True)
    

        