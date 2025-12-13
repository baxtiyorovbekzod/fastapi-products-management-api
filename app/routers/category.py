from typing import List, Annotated

from fastapi.routing import APIRouter
from fastapi import HTTPException, Path, Body, Depends
from sqlalchemy.orm import Session

from ..schemas import CategoryReponse, CategoryCreate, CategoryUpdate
from ..database import get_db
from ..models import Category

router = APIRouter(
    tags=['Categories']
)


@router.get('/', response_model=List[CategoryReponse])
def get_categories(
    session: Session = Depends(get_db),
):
    return session.query(Category).all() 


@router.get('/{category_id}', response_model=CategoryReponse)
def get_one_category(
    category_id: int = Path(ge=1),
    session: Session = Depends(get_db),
):
    category = session.query(Category).get(category_id)
    
    if not category:
        raise HTTPException(status_code=404, detail='category not found.')
    
    return category


@router.post('/', response_model=CategoryReponse)
def create_category(
    data: CategoryCreate,
    session: Session = Depends(get_db)
):
    existing_category = session.query(Category).filter(Category.name==data.name).first()
    if existing_category:
        raise HTTPException(status_code=400, detail='category exists.')

    new_category = Category(name=data.name, description=data.description)
    session.add(new_category)
    session.commit()
    session.refresh(new_category)

    return new_category


@router.put('/{category_id}', response_model=CategoryReponse)
def update_category(
    category_id: Annotated[int, Path(ge=1)],
    data: Annotated[CategoryUpdate, Body],
    session: Session = Depends(get_db)
):
    existing_category = session.query(Category).get(category_id)

    if not existing_category:
        raise HTTPException(status_code=404, detail='category not found.')

    if session.query(Category).filter(Category.name==data.name).first():
        raise HTTPException(status_code=400, detail='category exists.')

    existing_category.name = data.name if data.name else existing_category.name
    existing_category.description = data.description if data.description else existing_category.description

    session.commit()
    session.refresh(existing_category)

    return existing_category


@router.delete('/{category_id}')
def update_category(
    category_id: Annotated[int, Path(ge=1)],
    session: Session = Depends(get_db)
):
    existing_category = session.query(Category).get(category_id)

    if not existing_category:
        raise HTTPException(status_code=404, detail='category not found.')

    session.delete(existing_category)
    session.commit()

    return {'message': 'deleted.'}
    