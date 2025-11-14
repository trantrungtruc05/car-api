from fastapi import APIRouter
from .endpoints import categories, cars

api_router = APIRouter()

api_router.include_router(
    categories.router, 
    prefix="/categories", 
    tags=["categories"]
)

api_router.include_router(
    cars.router, 
    prefix="/cars", 
    tags=["cars"]
)
