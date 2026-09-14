from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.cart import Cart
from app.models.cart_item import CartItem
from app.models.product import Product
from app.models.order import Order
from app.schemas.cart import CartRead, CartItemCreate
from app.services.order_service import checkout
from app.schemas.order import OrderRead



router = APIRouter(prefix='/cart', tags=['cart'])

def get_or_create_cart(db: Session, user: User) -> Cart:
    '''Return the current user's cart or create one if it doesn't exist'''
    cart = db.query(Cart).filter(Cart.user_id == user.id).first()
    if not cart:
        cart = Cart(user_id = user.id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

@router.get('/', response_model=CartRead)
def view_cart(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    '''View the current users cart and items'''
    cart = get_or_create_cart(db, current_user)
    return cart

@router.post("/items", response_model=CartRead)
def add_item(item: CartItemCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Add a product to the current user's cart, or increase quantity if it's already in there."""
    cart = get_or_create_cart(db, current_user)

    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id,
    ).first()

    if existing_item:
        existing_item.quantity += item.quantity # type: ignore[assignment]
    else:
        existing_item = CartItem(cart_id=cart.id, product_id=item.product_id, quantity=item.quantity)
        db.add(existing_item)

    db.commit()
    db.refresh(cart)
    return cart


@router.delete("/items/{cart_item_id}", response_model=CartRead)
def remove_item(cart_item_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    '''Remove a specific item from the current user's cart'''
    cart = get_or_create_cart(db, current_user)

    cart_item = db.query(CartItem).filter(
        CartItem.id == cart_item_id,
        CartItem.cart_id == cart.id,
    ).first()

    if not cart_item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    db.delete(cart_item)
    db.commit()
    db.refresh(cart)
    return cart

@router.post('/checkout', response_model=OrderRead)
def checkout_cart(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    '''Converts the user's current cart into an order'''
    cart = get_or_create_cart(db, current_user)
    return checkout(cart, db)





