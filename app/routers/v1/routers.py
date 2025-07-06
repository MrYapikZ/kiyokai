from fastapi import APIRouter
from app.routers.v1.auth import auth
from app.routers.v1.zou import api
from app.routers.v1.shots import shots
from app.routers.v1.nas import nas
from app.routers.v1.__test__ import example

api_router = APIRouter()
api_router.include_router(api.router, prefix="/zou", tags=["zou"])
api_router.include_router(shots.router, prefix="/shots", tags=["shots"])
api_router.include_router(nas.router, prefix="/nas", tags=["nas"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])

api_router.include_router(example.router, prefix="/test", tags=["test"])