from typing import List

from pydantic import BaseModel, Field


class ProductResponse(BaseModel):
    product_id: int
    name: str = Field(max_length=100)
    price: float
    in_stock: bool

    class Config:
        from_attributes = True


class ProductCreate(BaseModel):
    category_id: int
    name: str = Field(max_length=100)
    price: float


class CategoryReponse(BaseModel):
    category_id: int
    name: str = Field(max_length=100)
    description: str | None = None
    products: List[ProductResponse] = []

    class Config:
        from_attributes = True


class CategoryCreate(BaseModel):
    name: str = Field(max_length=100)
    description: str | None = None


class CategoryUpdate(BaseModel):
    name: str | None = Field(max_length=100)
    description: str | None = None
