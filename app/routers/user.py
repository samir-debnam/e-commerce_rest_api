from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(prefix='/users', tags=['users'])



@router.post('/register', response_model=UserRead)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    '''Register a new user account. Email must be unique. Password is hashed before storage '''
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail='Email already registered')

    new_user = User(
        email=user.email,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.post('/login')
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    '''Verify login credentials and return a JWT token'''
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password): # type: ignore[call-arg]
        raise HTTPException(status_code=401, detail='Invalid email or password')

    access_token = create_access_token(data={'sub': str(user.id)})
    return {"access_token": access_token, 'token_type': 'bearer'}


