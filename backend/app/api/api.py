from app.api.endpoints import core, example, calculator
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(example.router, tags=["Example"])
api_router.include_router(core.router, tags=["Core"])
api_router.include_router(calculator.router, tags=["Business Logic"])
