from fastapi import APIRouter, HTTPException, Depends, status, Request, Path
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config import settings
from app.core.prisma import db
from app.services.auth import AuthService

router = APIRouter()

@router.post("/create", status_code=status.HTTP_201_CREATED, dependencies=[Depends(AuthService.verify_user_token)])
async def create_mastershot(request: Request):
    """
    Endpoint to create a master shot.
    This endpoint can be used to create a new master shot in the system.
    """
    try:
        data = await request.json()
        file_name = data.get("file_name")
        file_path = data.get("file_path")

        existing = await db.mastershot.find_first(
            where={
                "file_name": file_name,
                "file_path": file_path
            }
        )

        if existing:
            return JSONResponse(
                status_code=200,
                content={
                    "success": False,
                    "exist": True,
                    "message": "Master shot with this file name and path already exists.",
                    "data": jsonable_encoder(existing)
                }
            )

        mastershot = await db.mastershot.create(data, include={"nas_server": True})
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

@router.get("/list", status_code =status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def list_mastershots():
    """
    Endpoint to list all master shots.
    This endpoint can be used to retrieve all master shots from the system.
    """
    try:
        mastershots = await db.mastershot.find_many(include={"nas_server": True})
        return JSONResponse(content={
            "success": True,
            "message": "Master shots retrieved successfully!",
            "data": jsonable_encoder(mastershots)
        }, status_code=200)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_version_shot_by_shot_id(shot_id: str = Path(..., description="ID of the shot to retrieve")):
    """
    Endpoint to retrieve a single master shot by shot_id.
    Requires Bearer token authentication.
    """
    try:
        master_shot = await db.mastershot.find_first(where={"shot_id": shot_id}, include={"nas_server": True})
        if not master_shot:
            raise HTTPException(status_code=404, detail=f"MasterShot with shot_id '{shot_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": "Master shot retrieved successfully!",
            "data": jsonable_encoder(master_shot)
        }, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/{shot_id}/tasks/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_version_shot_by_shot_id(shot_id: str = Path(..., description="ID of the shot to retrieve"), task_id: str = Path(..., description="ID of the task to retrieve")):
    """
    Endpoint to retrieve a single master shot by shot_id and task_id.
    Requires Bearer token authentication.
    """
    try:
        master_shot = await db.mastershot.find_first(where={"shot_id": shot_id, "task_id": task_id}, include={"nas_server": True})
        if not master_shot:
            raise HTTPException(status_code=404, detail=f"MasterShot with shot_id '{shot_id}' and task_id '{task_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": "Master shot retrieved successfully!",
            "data": jsonable_encoder(master_shot)
        }, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/update/{shot_id}/tasks/{task_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def update_mastershot(shot_id: str, task_id: str, request: Request):
    """
    Endpoint to update a master shot by shot_id and task_id.
    Requires Bearer token authentication.
    """
    try:
        data = await request.json()

        updated_mastershot = await db.mastershot.update(
            where={"shot_id_task_id": {"shot_id": shot_id, "task_id": task_id}},
            data=data
        )
        if not updated_mastershot:
            raise HTTPException(status_code=404, detail=f"MasterShot with shot_id '{shot_id}' and task_id '{task_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": "Master shot updated successfully!",
            "data": jsonable_encoder(updated_mastershot)
        }, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/delete/{shot_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(AuthService.verify_user_token)])
async def delete_mastershot(shot_id: str, task_id: str):
    """
    Endpoint to delete a master shot by shot_id and task_id.
    Requires Bearer token authentication.
    """
    try:
        deleted_mastershot = await db.mastershot.delete(where={"shot_id": shot_id, "task_id": task_id})
        if not deleted_mastershot:
            raise HTTPException(status_code=404, detail=f"MasterShot with shot_id '{shot_id}' and task_id '{task_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": "Master shot deleted successfully!"
        }, status_code=204)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/list/projects/{project_id}", status_code=status.HTTP_200_OK, dependencies=[Depends(AuthService.verify_user_token)])
async def get_version_shot_by_project_id(project_id: str = Path(..., description="ID of the shot to retrieve")):
    """
    Endpoint to retrieve a single master shot by project_id.
    Requires Bearer token authentication.
    """
    try:
        master_shot = await db.mastershot.find_first(where={"project_id": project_id}, include={"nas_server": True})
        if not master_shot:
            raise HTTPException(status_code=404, detail=f"MasterShot with shot_id '{project_id}' not found.")

        return JSONResponse(content={
            "success": True,
            "message": "Master shot retrieved successfully!",
            "data": jsonable_encoder(master_shot)
        }, status_code=200)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))