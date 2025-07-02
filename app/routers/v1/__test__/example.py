from fastapi import APIRouter, Depends, Request
from app.core.dependencies import get_current_user, get_optional_current_user
from typing import Optional

router = APIRouter()

@router.get("/protected-data")
def get_protected_data(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Example of a protected API endpoint that validates token first.
    Requires:
    - Authorization: Bearer <token> header
    - X-Zou-Url: <zou_url> header
    """
    return {
        "message": "This data is only available to authenticated users",
        "data": ["item1", "item2", "item3"],
        "user_info": {
            "user_id": current_user.get("user").get("id"),
            "email": current_user.get("user").get("email")
        }
    }

@router.get("/public-data")
def get_public_data(
    request: Request,
    current_user: Optional[dict] = Depends(get_optional_current_user)
):
    """
    Example of a public API that can optionally use authentication.
    Works with or without token.
    """
    response = {
        "message": "This is public data",
        "data": ["public1", "public2"]
    }

    if current_user:
        response["personalized_message"] = f"Welcome back, {current_user.get('email', 'user')}!"

    return response

@router.post("/create-item")
def create_item(
    item_data: dict,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    """
    Example of creating data with authentication required.
    """
    return {
        "message": "Item created successfully",
        "item": item_data,
        "created_by": current_user.get("email")
    }
