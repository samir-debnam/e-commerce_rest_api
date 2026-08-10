from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductRead, ProductUpdate

router = APIRouter(prefix='/products', tags=['products'])

@router.post('/', response_model=ProductRead)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    ''' Create a new product'''
    new_product = Product(**product.model_dump())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product

@router.get('/', response_model=list[ProductRead])
def list_products(db: Session = Depends(get_db)):
    '''List all products'''
    return db.query(Product).all()

@router.get('/{product_id}', response_model=ProductRead)
def get_product(product_id: int, db: Session = Depends(get_db)):
    '''Retrieve a single product by its ID'''
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')
    return product

@router.patch('/{product_id}', response_model=ProductRead)
def update_product(product_id: int, product_update: ProductUpdate, db: Session = Depends(get_db)):
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
def delete_product(product_id: int, db: Session = Depends(get_db)):
    '''Delete a product by its ID'''
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(product)
    db.commit()