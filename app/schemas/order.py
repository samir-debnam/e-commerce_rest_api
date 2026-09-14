from pydantic import BaseModel
from pydantic import ConfigDict
from datetime import datetime
from app.schemas.product import ProductRead

class OrderItemRead(BaseModel):
    id: int
    quantity: int
    price_at_purchase: float
    product: ProductRead

    model_config = ConfigDict(from_attributes=True)

class OrderRead(BaseModel):
    id: int
    total: float
    created_at: datetime
    items: list[OrderItemRead]

    model_config = ConfigDict(from_attributes=True)


