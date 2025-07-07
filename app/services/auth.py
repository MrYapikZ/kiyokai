from fastapi import APIRouter, HTTPException, Depends, status, Request
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from typing import Optional
from app.config import settings
from app.core.prisma import db
import requests
import httpx

class AuthService:
    """Service for handling authentication-related operations"""

    @staticmethod
    async def verify_user_token(request: Request):
        # 1. Get Authorization header
        auth_header: Optional[str] = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Missing or invalid Authorization header")

        token = auth_header.split(" ")[1]

        # 2. Validate token with external ZOU API
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{settings.ZOU_API_URL}/auth/authenticated",
                    headers={"Authorization": f"Bearer {token}"}
                )
                if response.status_code != 200:
                    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
        except httpx.RequestError as e:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Auth service error: {str(e)}")

def verify_login_kitsu(email, password, api_url):
    """Verify user login with Kitsu API"""
    api_url = f"{api_url}/auth/login"

    headers = {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}
    payload = {"email": email, "password": password}

    try:
        response = requests.post(api_url, headers=headers, data=payload)
        # print(f"JSON: {response.json()}")
        if response.status_code != 200:
            return {"success": False, "message": "Login failed. Please check your credentials."}
        return response.json(), response.cookies
    except requests.RequestException as e:
        return {"success": False, "message": f"Network error: {e}"}

