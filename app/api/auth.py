from app.settings import settings
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional


CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
CLIENT_URL = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}"
REDIRECT_URI = "http://localhost:8000/auth/callback"
FRONTEND_URL = "http://localhost:5173/welcome"


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

@router.get("/callback")
async def github_app_callback(
    code: Optional[str] = Query(None), # <- this is the code you need to in order to create the JWT.
    state: Optional[str] = Query(None),
    error: Optional[str] = Query(None),
    error_description: Optional[str] = Query(None),
):
    
    # This is to handle errors, if you want, you can add more friendly error messages.
    # The random string is for CSRF.
    # If you have already provided access, you must revoke it from your github account.
    if state != "random_state_string":
        return RedirectResponse(
            url=f"{FRONTEND_URL}?error=invalid_state&message=Invalid+state+parameter"
        )
    if error:
        print(f"GitHub OAuth Error: {error}")
        print(f"Error Description: {error_description}")
        error_messages = { # Check if these messages are still valid.
            "access_denied": "You cancelled the GitHub authorization. Please try again if you want to continue.",
            "incorrect_client_credentials": "GitHub app configuration error. Please contact support.",
            "redirect_uri_mismatch": "Configuration error. Please contact support.",
            "bad_verification_code": "Authorization expired. Please try logging in again."
        }
        user_message = error_messages.get(error, f"GitHub authorization failed: {error_description}")

        return RedirectResponse( # Redirect that bitch.
            url=f"{FRONTEND_URL}?error={error}&message={user_message.replace(' ', '+')}"
        )
    
    # now handle successful authorization, must:
    # 1 - Check if the code is present.
    # 2 - If it is create token with Code from url param.
    # 3 - Update the front-end.
    