from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers.v1.shots.master import master
from app.routers.v1.shots.version import version

router = APIRouter()

router.include_router(master.router, prefix="/mastershots", tags=["mastershots"])
router.include_router(version.router, prefix="/versionshots", tags=["versionshots"])