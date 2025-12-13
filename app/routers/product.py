from typing import Annotated

from fastapi.routing import APIRouter
from fastapi import Body, Path, Query, Depends
from sqlalchemy.orm import Session

from ..schemas import ProductCreate, ProductResponse
from ..database import get_db
from ..models import Product

router = APIRouter(tags=['Products'])


@router.get('/')
def get_products():
    return {}


@router.post('/', response_model=ProductResponse)
def create_product(
    # product_data: ProductCreate = Body(),
    product_data: Annotated[ProductCreate, Body],
    session: Annotated[Session, Depends(get_db)]
):
    product = Product(
        name=product_data.name,
        price=product_data.price,
        category_id=product_data.category_id,
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    return product
