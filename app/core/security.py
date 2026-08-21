from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User
from app.core.config import settings

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='users/login')

def hash_password(password: str) -> str:
    '''Hash a plain-text password using bcrypt. Returns a new hash each call'''
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    '''Check a plain-text password against a stored hash'''
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict) -> str:
    '''Create a signed JWT that expires after ACCESS_TOKEN_EXPIRE_MINUTES'''
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp': expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    '''Decode the JWT from request, verify and return the matching user'''
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Could not validate credentials',
        headers={'WWW-Authenticate': 'Bearer'}
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id = payload.get('sub')
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise credentials_exception

    return user

def require_admin(current_user: User = Depends(get_current_user)) -> User:
    '''Ensure the current user is an admin otherwise raise 403 error'''
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail='Admin role required')
    return current_user
