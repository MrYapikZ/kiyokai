from fastapi import APIRouter, HTTPException, Depends, status, Request, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config import settings
from app.core.prisma import db
from app.services.auth import AuthService

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AuthService.verify_user_token)])
async def create_versionshot(request: Request):
    """
    Endpoint to create a version shot.
    Automatically assigns the next version number based on shot_id.
    """
    try:
        data = await request.json()

        shot_id = data.get("shot_id")
        if not shot_id:
            raise HTTPException(status_code=400, detail="shot_id is required")

        # Get the latest version_number for this shot_id
        latest_version = await db.versionshot.find_first(
            where={"shot_id": shot_id},
            order={"version_number": "desc"}
        )

        next_version_number = 0 if latest_version is None else latest_version.version_number + 1

        # Add version_number to the payload
        data["version_number"] = next_version_number

        # Create the new version shot
        versionshot = await db.versionshot.create(data, include={"master_shot": True})

        return JSONResponse(content={
            "success": True,
            "message": f"Version {next_version_number} for shot '{shot_id}' created successfully!",
            "data": jsonable_encoder(versionshot)
        }, status_code=201)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def list_versionshots():
    """
    Endpoint to list all version shots.
    """
    try:
        versionshots = await db.versionshot.find_many()
        return JSONResponse(content={
            "success": True,
            "message": "Version shots retrieved successfully!",
            "data": jsonable_encoder(versionshots)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_versionshots_by_shot_id(shot_id: str = Path(..., description="ID of the shot")):
    """
    Endpoint to retrieve all version shots by shot_id.
    """
    try:
        versionshots = await db.versionshot.find_many(where={"shot_id": shot_id})
        return JSONResponse(content={
            "success": True,
            "message": "Version shots retrieved successfully!",
            "data": jsonable_encoder(versionshots)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}/versions", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_latest_version_by_shot_id(shot_id: str = Path(..., description="ID of the shot")):
    """
    Endpoint to retrieve the latest version of a shot by shot_id.
    Assumes highest version_number is the latest.
    """
    try:
        latest_version = await db.versionshot.find_first(
            where={"shot_id": shot_id},
            order={"version_number": "desc"}
        )
        if not latest_version:
            raise HTTPException(status_code=404, detail=f"No version found for shot_id '{shot_id}'.")

        return JSONResponse(content={
            "success": True,
            "message": "Latest version shot retrieved successfully!",
            "data": jsonable_encoder(latest_version)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}/versions/{version}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_specific_version(
    shot_id: str = Path(..., description="ID of the shot"),
    version: int = Path(..., description="Version number to retrieve")
):
    """
    Endpoint to retrieve a specific version of a shot by shot_id and version number.
    """
    try:
        version_shot = await db.versionshot.find_first(where={
            "shot_id": shot_id,
            "version_number": version
        })
        if not version_shot:
            raise HTTPException(status_code=404, detail=f"Version {version} for shot_id '{shot_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": f"Version {version} retrieved successfully!",
            "data": jsonable_encoder(version_shot)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))