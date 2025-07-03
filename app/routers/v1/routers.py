from fastapi import APIRouter
from app.routers.v1.auth import auth
from app.routers.v1.zou import api
from app.routers.v1.__test__ import example

api_router = APIRouter()
api_router.include_router(api.router, prefix="/zou", tags=["zou"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(example.router, prefix="/test", tags=["test"])