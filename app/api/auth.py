from app.settings import settings
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx


CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
CLIENT_URL = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}"
REDIRECT_URI = "http://localhost:8000/auth/callback"
FRONTEND_URL = "http://localhost:5173"


router = APIRouter(prefix="/auth", tags=["auth"])


# Hacerle request a este link: href="https://github.com/login/oauth/authorize?client_id={CLIENT_ID}
@router.get("/github")
async def github_app_login():
    """Redirect user to install/authorize GitHub App"""
    auth_url = (
        f"https://github.com/login/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&redirect_uri={REDIRECT_URI}"
        f"&scope=user:email read:user"
        f"&state=random_state_string"
    )
    return RedirectResponse(url=auth_url)

# @router.get("/callback")
# async def github_app_callback(code: str = Query(...), installation_id: str = Query(None)):
    