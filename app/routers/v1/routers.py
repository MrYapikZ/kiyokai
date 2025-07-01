from fastapi import APIRouter
from app.routers.v1.auth import auth

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])