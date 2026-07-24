from fastapi import FastAPI
from app.core.config import settings


app = FastAPI()

@app.get('/')
def read_root():
    return {'message': 'Welcome to my portfolio E-Commerce API!', 'db_configured' : bool(settings.database_url)}



