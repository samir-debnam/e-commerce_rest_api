from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt

from app.core.config import settings

ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

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