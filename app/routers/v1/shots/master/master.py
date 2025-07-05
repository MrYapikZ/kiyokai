from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config import settings
from app.core.prisma import db

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED)
async def create_mastershot(request: Request):
    """
    Endpoint to create a master shot.
    This endpoint can be used to create a new master shot in the system.
    """
    try:
        data = await request.json()

        mastershot = await db.mastershot.create(data)
        print(mastershot)

        # Here you would typically process the data and save it to a database
        # For demonstration, we will just return the received data
        return JSONResponse(content={
            "success": True,
            "message": "Master shot created successfully!",
            "data": jsonable_encoder(mastershot)
        }, status_code=201)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))