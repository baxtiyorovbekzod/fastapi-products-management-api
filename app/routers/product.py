from typing import Annotated, List, Optional

from fastapi.routing import APIRouter
from fastapi import Body, Path, Query, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..schemas import ProductCreate, ProductResponse
from ..database import get_db
from ..models import Product, Category

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
    category = session.query(Category).get(product_data.category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    
    product = Product(
        name=product_data.name,
        price=product_data.price,
        category_id=category.category_id,
        in_stock=product_data.in_stock
    )
    session.add(product)
    session.commit()
    session.refresh(product)

    return product


@router.get('/search', response_model=List[ProductResponse])
def search_products(
    name: Annotated[str, Query(min_length=1)],
    session: Annotated[Session, Depends(get_db)]
):
    result = session.query(Product).filter(Product.name.ilike(f'%{name.lower()}%')).all()
    return result


@router.get('/filter/category', response_model=List[ProductResponse])
def search_products(
    category: Annotated[str, Query(min_length=2)],
    session: Annotated[Session, Depends(get_db)]
):
    category = session.query(Category).filter(Category.name==category).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')
    
    return category.products


@router.get('/filter/price', response_model=List[ProductResponse])
def search_products(
    session: Annotated[Session, Depends(get_db)],
    min_price: Annotated[float, Query(ge=0)] = None,
    max_price: Annotated[float, Query(ge=0)] = None,
):
    products = session.query(Product)
    if min_price:
        products = products.filter(Product.price >= min_price)
    if max_price:
        products = products.filter(Product.price <= max_price)

 # products = products.order_by(Product.price.asc()) sort uchun

    return products.all()
