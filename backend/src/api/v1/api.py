from fastapi import APIRouter

from src.api.v1.endpoints import auth, test

api_router = APIRouter()
api_router.include_router(test.router, prefix="/test", tags=["test"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
