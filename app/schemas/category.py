from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Optional

class CategoryBase(BaseModel):
    name: str


class CategoryCreate(CategoryBase):
    pass 

class CategoryRead(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CategoryUpdate(BaseModel):
    name: Optional[str] = None