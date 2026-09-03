from pydantic import BaseModel
from datetime import datetime
from app.schemas.product import ProductRead

class OrderItemRead(BaseModel):
    id: int
    quanitity: int
    price_at_purchase: int
    product: ProductRead

    class Config:
        from_attributes = True

class OrderRead(BaseModel):
    id: int
    total: float
    created_at: datetime
    items: list[OrderItemRead]

    class Config:
        from_attributes = True


