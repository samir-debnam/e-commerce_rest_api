from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate
from app.models.user import User
from app.core.security import get_current_user
from app.core.security import require_admin

router = APIRouter(prefix='/products', tags=['products'])

@router.post('/', response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    ''' Create a new product'''
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get('/', response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db),
                  category_id: Optional[int] = None,
                  min_price: Optional[float] = None,
                  max_price: Optional[float] = None,
                  sort_by: Optional[str] = None,
                  ):
    '''List all products, optionally filtered by category, price or name'''
    query = db.query(Product)

    if category_id is not None:
        query = query.filter(Product.category_id == category_id)

    if min_price is not None:
        query = query.filter(Product.price >= min_price)

    if max_price is not None:
        query = query.filter(Product.price <= max_price)

    if sort_by == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort_by == 'name':
        query = query.order_by(Product.name.asc())

    return query.all()

@router.get('/{product_id}', response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    '''Retrieve a single product by its ID'''
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product

@router.patch('/{product_id}', response_model=ProductRead)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    '''Partially update an existing product's fields'''
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)
    return product

@router.delete('/{product_id}', status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    '''Delete a product by its ID'''
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(product)
    db.commit()