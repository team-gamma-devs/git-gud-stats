from app.settings import settings
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import RedirectResponse
import httpx
from typing import Optional


CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
CLIENT_URL = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}"
REDIRECT_URI = "http://localhost:8000/auth/callback"
FRONTEND_URL = "http://localhost:5173/"


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
            url=f"{FRONTEND_URL}github-error?error=invalid_state&message=Invalid+state+parameter"
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

        return RedirectResponse( 
            url=f"{FRONTEND_URL}/github-error?error={error}&message={user_message.replace(' ', '+')}"
        )
    
    if not code:
        print("Code not found!");
        return RedirectResponse(
            url=f"{FRONTEND_URL}github-error?error={error}&message=code_not_found"
        )
    try:
        header = {"Accept": "application/json"}
        token_template = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code
        }

        async with httpx.AsyncClient() as client:
            response = await client.post("https://github.com/login/oauth/access_token", data=token_template, headers=header)

            if response.status_code != 200:
                raise HTTPException(status_code=400, detail=f"Failed HTTP request, payload: {response}")

            token_response = response.json()
            access_token = token_response.get("access_token")
            
            if not access_token:
                raise HTTPException(status_code=400, detail="Status code not found")

            user_response = await client.get(
                "https://api.github.com/user",
                headers={"Authorization": f"token {access_token}"}
            )
            
            if user_response.status_code != 200:
                raise HTTPException(status_code=400, detail="Couldn't get user info");
            
            user_data = user_response.json()
            
            print(f"Successfully authenticated user: {user_data}")
            
            return RedirectResponse(
                url=f"{FRONTEND_URL}/welcome?success=true&token={access_token}&user={user_data}"
            )

    except httpx.RequestError as request_error:
        print("ERROR IN GITHUB TOKEN REQUEST: {request_error}");
        return RedirectResponse(
            url=f"{FRONTEND_URL}network-error?error=network_error&message=Network+error+encountered"
        )
    except Exception as e:
        print(f"Generic token retrieval error: {str(e)}")
        return RedirectResponse(
            url=f"{FRONTEND_URL}server-error-error?error=server_error&message=An+unexpected+error+occurred"
        )
    # now handle successful authorization, must:
    # 1 - Check if the code is present.
    # 2 - If it is create token with Code from url param.
    # 3 - Update the front-end.
    # 
    