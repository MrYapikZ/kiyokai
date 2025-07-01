from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.config import settings
from app.schemas.auth import LoginRequest, Token
from app.services.auth import verify_login_kitsu
from app.core.dependencies import oauth2_scheme
from typing import Dict

router = APIRouter()

@router.post("/login", response_model=Token)
def login(payload: LoginRequest):
    """
    Login endpoint to authenticate users.
    """
    email = payload.username
    password = payload.password
    zou_url = payload.zou_url

    response, cookies = verify_login_kitsu(email, password, zou_url)

    if not isinstance(response, dict) or "access_token" not in response:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=response.get("message", "Invalid credentials") if isinstance(response,
                                                                                dict) else "Unexpected response format",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Create JSON response
    res = JSONResponse(content=response)

    # Optional: you can set any relevant token or user cookie
    res.set_cookie(
        key=settings.COOKIE_REFRESH_TOKEN_NAME,
        value=response.get("refresh_token", ""),
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        max_age=settings.COOKIE_MAX_AGE
    )

    return res