from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends, status, Request
from typing import Optional
import requests
import logging

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

logger = logging.getLogger(__name__)

def get_current_user(token: str = Depends(oauth2_scheme), request: Request = None):
    """
    Validate token with external authentication service.
    Extracts zou_url from request headers or session data.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Get zou_url from request headers
    zou_url = None
    if request:
        zou_url = request.headers.get("X-Zou-Url") or request.headers.get("zou-url")

        # Fallback: try to get from cookies or session if available
        if not zou_url and hasattr(request.state, 'zou_url'):
            zou_url = request.state.zou_url

    if not zou_url:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="zou_url is required for authentication validation"
        )

    try:
        # Validate token with external auth service
        auth_url = f"{zou_url}/auth/authenticated"
        headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/json"
        }

        response = requests.get(auth_url, headers=headers, timeout=10)

        if response.status_code == 200:
            user_data = response.json()
            return user_data
        elif response.status_code == 401:
            raise credentials_exception
        else:
            logger.error(f"Auth service error: {response.status_code} - {response.text}")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication service unavailable"
            )

    except requests.RequestException as e:
        logger.error(f"Network error during auth validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication service unavailable"
        )
    except Exception as e:
        logger.error(f"Unexpected error during auth validation: {e}")
        raise credentials_exception

def get_optional_current_user(token: Optional[str] = Depends(oauth2_scheme), request: Request = None):
    """
    Optional token validation - returns None if no token or invalid token.
    Useful for endpoints that can work with or without authentication.
    """
    if not token:
        return None

    try:
        return get_current_user(token, request)
    except HTTPException:
        return None
