from settings import settings
from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import httpx


CLIENT_ID = settings.client_id
CLIENT_SECRET = settings.client_secret
CLIENT_URL = f"https://github.com/login/oauth/authorize?client_id={CLIENT_ID}"


router = APIRouter()


# Hacerle request a este link: href="https://github.com/login/oauth/authorize?client_id={CLIENT_ID}
@router.get("/", response_class=HTMLResponse)
async def login():
     async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(f"{CLIENT_URL}", headers=headers)
        if resp.status_code == 404:
            raise HTTPException(status_code=404, detail="User not found")
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()

@router.get("/callback", response_class=HTMLResponse)
async def callback(code: str):
    pass

