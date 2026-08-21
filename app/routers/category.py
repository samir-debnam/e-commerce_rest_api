from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.category import Category
from app.schemas.category import CategoryBase, CategoryCreate, CategoryRead, CategoryUpdate
from app.core.security import require_admin
from app.models.user import User


router = APIRouter(prefix='/categories', tags=['categories'])

@router.post('/', response_model=CategoryRead)
def create_category(category: CategoryCreate, db: Session = Depends(get_db), current_user: User = (Depends(require_admin))):
    '''Create a new category'''
    new_category = Category(**category.model_dump())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

@router.get('/', response_model=list[CategoryRead])
def list_categories(db: Session = Depends(get_db)):
    '''List all categories'''
    return db.query(Category).all()

@router.get('/{category_id}', response_model=CategoryRead)
def get_category(category_id: int, db: Session = Depends(get_db)):
    '''Retrieve a single category by its ID'''
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')
    return category

@router.patch('/{category_id}', response_model=CategoryRead)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    '''Partially update an existing category's fields'''
    category = db.query(Category).filter(Category.id==category_id ).first()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    update_data = category_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(category, key, value)
    db.commit()
    db.refresh(category)
    return category

@router.delete('/{category_id}', status_code=204)
def delete_category(category_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    '''Delete a category by its ID'''
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail='Category not found')

    db.delete(category)
    db.commit()




