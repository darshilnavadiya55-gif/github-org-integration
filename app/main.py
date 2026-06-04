from fastapi import FastAPI

from app.api.analytics import router as analytics_router
from app.api.auth import router as auth_router
from app.api.webhooks import router as webhook_router
from app.core.config import settings

app = FastAPI(title=settings.APP_NAME)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

app.include_router(auth_router, tags=["auth"])
app.include_router(webhook_router, tags=["webhooks"])