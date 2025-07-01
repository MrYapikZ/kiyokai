from app.config import settings
import requests

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