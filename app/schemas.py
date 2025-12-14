from typing import List, Annotated, Optional

from pydantic import BaseModel, Field



class CategoryReponse(BaseModel):
    category_id: int
    name: Annotated[str, Field(max_length=100)]
    description: str | None = None

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: Annotated[str, Field(min_length=2, max_length=100)]
    description: Annotated[str, Field(None, max_length=500)]


class CategoryUpdate(BaseModel):
    name: Annotated[Optional[str], Field(min_length=2, max_length=100)] = None
    description: Annotated[Optional[str], Field(max_length=500)] = None


class ProductResponse(BaseModel):
    product_id: int
    name: Annotated[str, Field(max_length=100)]
    price: float
    in_stock: bool
    category: CategoryReponse

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    category_id: int
    name: Annotated[str, Field(max_length=100)]
    price: float
    in_stock: Annotated[bool, Field(True)]

