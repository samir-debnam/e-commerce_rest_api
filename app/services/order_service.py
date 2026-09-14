from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.cart import Cart
from app.models.order import Order, OrderItem
from app.models.product import Product


def checkout(cart: Cart, db: Session) -> Order:
    '''Convert a user's cart into an order. Validates stock for each item, decreases inventory, creates the order and clears the cart'''
    if not cart.items:
        raise HTTPException(status_code=400, detail='Cart is empty')

    total = 0.0
    order_items = []

    for cart_item in cart.items:
        product = db.query(Product).filter(Product.id == cart_item.product_id).first()

        if not product:
            raise HTTPException(status_code=404, detail=f'Product {cart_item.product_id} no longer exists')

        if product.stock < cart_item.quantity:
            raise HTTPException(status_code=400, detail=f'Not enough stock for {product.name}')

        product.stock -= cart_item.quantity 
        line_total = product.price * cart_item.quantity
        total += line_total

        order_items.append(
            OrderItem(
                product_id=product.id, # type: ignore
                quantity=cart_item.quantity, # type: ignore
                price_at_purchase=product.price, # type: ignore
            )
        )

    new_order = Order(
        user_id=cart.user_id,
        total=total,
        items=order_items
    )
    db.add(new_order)
    for cart_item in list(cart.items):
        db.delete(cart_item)

    db.commit()
    db.refresh(new_order)
    return new_order