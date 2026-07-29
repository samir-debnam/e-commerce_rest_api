from fastapi import FastAPI

from app.core.config import settings
from app.routers import product


app = FastAPI()

app.include_router(product.router)

@app.get('/')
def read_root():
    return {'message': 'Welcome to my portfolio E-Commerce API!', 'db_configured' : bool(settings.database_url)}



