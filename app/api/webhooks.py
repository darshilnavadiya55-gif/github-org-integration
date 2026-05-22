from datetime import datetime, timezone

from fastapi import APIRouter, Depends, Header, HTTPException, Request
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.core.security import verify_github_signature
from app.db.mongo import get_db

router = APIRouter(prefix="/webhooks")


@router.post("/github")
async def github_webhook(
    request: Request,
    db: AsyncIOMotorDatabase = Depends(get_db),
    x_github_event: str | None = Header(default=None),
    x_hub_signature_256: str | None = Header(default=None),
    x_github_delivery: str | None = Header(default=None),
) -> dict[str, str]:
    body = await request.body()
    if not verify_github_signature(body, x_hub_signature_256 or "", settings.GITHUB_WEBHOOK_SECRET):
        raise HTTPException(status_code=401, detail="Invalid GitHub webhook signature")

    payload = await request.json()
    await db.webhook_events_raw.insert_one(
        {
            "delivery_id": x_github_delivery,
            "event_type": x_github_event,
            "payload": payload,
            "received_at": datetime.now(timezone.utc),
        }
    )

    return {"status": "accepted"}
