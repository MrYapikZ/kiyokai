from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from app.config import settings
from app.routers.v1.shots.master import master

router = APIRouter()

router.include_router(master.router, prefix="/mastershots", tags=["mastershots"])