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
    Automatically assigns the next version number based on shot_id and task_id.
    Prevents duplicate file_path and file_name.
    """
    try:
        data = await request.json()

        shot_id = data.get("shot_id")
        task_id = data.get("task_id")
        file_path = data.get("file_path")
        file_name = data.get("file_name")

        if not shot_id or not task_id:
            raise HTTPException(status_code=400, detail="Both shot_id and task_id are required")
        if not file_path or not file_name:
            raise HTTPException(status_code=400, detail="file_path and file_name are required")

        # Explicit AND condition
        existing = await db.versionshot.find_first(
            where={
                "AND": [
                    {"file_name": file_name},
                    {"file_path": file_path}
                ]
            }
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="VersionShot with the same file_name and file_path already exists."
            )

        # Find latest version
        latest_version = await db.versionshot.find_first(
            where={
                "shot_id": shot_id,
                "task_id": task_id
            },
            order={"version_number": "desc"}
        )

        next_version_number = 0 if latest_version is None else latest_version.version_number + 1
        data["version_number"] = next_version_number

        # Create version shot
        versionshot = await db.versionshot.create(data, include={"master_shot": True})

        return JSONResponse(content={
            "success": True,
            "message": f"Version {next_version_number} for shot '{shot_id}' and task '{task_id}' created successfully!",
            "data": jsonable_encoder(versionshot)
        }, status_code=201)

    except HTTPException as he:
        raise he
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

@router.get("/list/{shot_id}/tasks/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_versionshots_by_shot_id_and_task_id(
    shot_id: str = Path(..., description="ID of the shot"),
    task_id: str = Path(..., description="ID of the task")
):
    """
    Endpoint to retrieve all version shots by shot_id and task_id.
    """
    try:
        versionshots = await db.versionshot.find_many(where={
            "shot_id": shot_id,
            "task_id": task_id
        })
        return JSONResponse(content={
            "success": True,
            "message": "Version shots retrieved successfully!",
            "data": jsonable_encoder(versionshots)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}/tasks/{task_id}/versions", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_versionshots_by_shot_id_and_task_id_versions(
    shot_id: str = Path(..., description="ID of the shot"),
    task_id: str = Path(..., description="ID of the task")
):
    """
    Endpoint to retrieve the latest version shot by shot_id and task_id.
    """
    try:
        versionshots = await db.versionshot.find_first(
            where={
                "shot_id": shot_id,
                "task_id": task_id
            },
            order={"version_number": "desc"}
        )
        if not versionshots:
            raise HTTPException(status_code=404, detail=f"No versions found for shot_id '{shot_id}' and task_id '{task_id}'.")

        return JSONResponse(content={
            "success": True,
            "message": "Latest version shot retrieved successfully!",
            "data": jsonable_encoder(versionshots)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}/tasks/{task_id}/versions/{version_number}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_version_by_shot_id_and_task_id(
    shot_id: str = Path(..., description="ID of the shot"),
    task_id: str = Path(..., description="ID of the task"),
    version_number: int = Path(..., description="Version number to retrieve")
):
    """
    Endpoint to retrieve a specific version shot by shot_id, task_id, and version_number.
    """
    try:
        version_shot = await db.versionshot.find_first(where={
            "shot_id": shot_id,
            "task_id": task_id,
            "version_number": version_number
        })
        if not version_shot:
            raise HTTPException(status_code=404, detail=f"Version {version_number} for shot_id '{shot_id}' and task_id '{task_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": f"Version {version_number} retrieved successfully!",
            "data": jsonable_encoder(version_shot)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{shot_id}/tasks/{task_id}/versions/{version_number}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(AuthService.verify_user_token)])
async def delete_version_by_shot_id_and_task_id(
    shot_id: str = Path(..., description="ID of the shot"),
    task_id: str = Path(..., description="ID of the task"),
    version_number: int = Path(..., description="Version number to delete")
):
    """
    Endpoint to delete a specific version shot by shot_id, task_id, and version_number.
    """
    try:
        deleted_version = await db.versionshot.delete_many(where={
            "shot_id": shot_id,
            "task_id": task_id,
            "version_number": version_number
        })
        if deleted_version.count == 0:
            raise HTTPException(status_code=404, detail=f"Version {version_number} for shot_id '{shot_id}' and task_id '{task_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": f"Version {version_number} deleted successfully!"
        }, status_code=204)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))