from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config import settings
from app.core.prisma import db
from app.services.auth import AuthService

router = APIRouter()

@router.get("/list", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def list_nas():
    """
    Endpoint to list all NAS entries.
    This endpoint can be used to retrieve all NAS entries from the system.
    """
    try:
        nas_entries = await db.nasserver.find_many(include={"master_shots": True})
        return JSONResponse(content={
            "success": True,
            "message": "NAS entries retrieved successfully!",
            "data": jsonable_encoder(nas_entries)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/create", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AuthService.verify_user_token)])
async def create_nas(request: Request):
    """
    Endpoint to create a NAS entry.
    This endpoint can be used to create a new NAS entry in the system.
    """
    try:
        data = await request.json()
        nas_entry = await db.nasserver.create(data)
        return JSONResponse(content={
            "success": True,
            "message": "NAS entry created successfully!",
            "data": jsonable_encoder(nas_entry)
        }, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))