from __future__ import annotations

from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.core.security import generate_state_token, xor_encrypt_decrypt
from app.db.mongo import get_db
from app.services.github_client import GitHubClient

router = APIRouter(prefix="/auth/github")


@router.get("/login")
async def github_login() -> dict[str, str]:
    state = generate_state_token()
    params = urlencode(
        {
            "client_id": settings.GITHUB_CLIENT_ID,
            "redirect_uri": settings.GITHUB_OAUTH_CALLBACK,
            "scope": "read:org repo",
            "state": state,
        }
    )
    auth_url = f"https://github.com/login/oauth/authorize?{params}"
    return {"auth_url": auth_url, "state": state}


@router.get("/callback")
async def github_callback(
    code: str = Query(...),
    state: str = Query(...),
    db: AsyncIOMotorDatabase = Depends(get_db),
) -> dict[str, str]:
    if not code or not state:
        raise HTTPException(status_code=400, detail="Invalid OAuth callback payload")

    github_client = GitHubClient()
    token_payload = await github_client.exchange_code_for_token(code)
    access_token = token_payload.get("access_token")
    if not access_token:
        raise HTTPException(status_code=400, detail="GitHub did not return an access token")

    user_client = GitHubClient(access_token=access_token)
    user = await user_client.get_authenticated_user()

    encrypted_token = xor_encrypt_decrypt(access_token, settings.ENCRYPTION_KEY)
    await db.github_tokens.update_one(
        {"github_user_id": user.get("id")},
        {
            "$set": {
                "github_user_id": user.get("id"),
                "login": user.get("login"),
                "token": encrypted_token,
                "token_type": token_payload.get("token_type", "bearer"),
                "scope": token_payload.get("scope", ""),
                "state": state,
            }
        },
        upsert=True,
    

    return {"message": "GitHub authorization successful", "login": user.get("login", "unknown")}
