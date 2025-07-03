from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from app.config import settings

router = APIRouter()

@router.get("/api")
def get_zou():
    """
    Example endpoint to demonstrate a simple GET request.
    This endpoint can be used to test the basic functionality of the API.
    """

    if not settings.ZOU_API_URL:
        return JSONResponse(content={
            "success": False,
            "message": "Zou URL is not configured in settings."
        }, status_code=404)
    return JSONResponse(content={
        "success": True,
        "message": "Zou API is configured!",
        "url": settings.ZOU_API_URL
    }, status_code=200)
