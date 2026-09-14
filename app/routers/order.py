from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.order import Order
from app.schemas.order import OrderRead

router = APIRouter(prefix='/orders', tags=['orders'])

@router.get("/", response_model=list[OrderRead])
def list_my_orders(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """List the current user's order history."""
    return db.query(Order).filter(Order.user_id == current_user.id).all()


@router.get("/{order_id}", response_model=OrderRead)
def get_my_order(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    """Retrieve a single order belonging to the current user."""
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id,
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order