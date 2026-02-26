from fastapi import APIRouter
from app.api.routes import main

api_router = APIRouter()
api_router.include_router(main.router)
