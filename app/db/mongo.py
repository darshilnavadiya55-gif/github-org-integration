from typing import AsyncGenerator

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.config import settings


client: AsyncIOMotorClient | None = None


def connect_to_mongo() -> AsyncIOMotorClient:
    global client
    if client is None:
        client = AsyncIOMotorClient(settings.MONGO_URI)
    return client


def get_database() -> AsyncIOMotorDatabase:
    mongo_client = connect_to_mongo()
    return mongo_client[settings.MONGO_DB]


async def get_db() -> AsyncGenerator[AsyncIOMotorDatabase, None]:
    yield get_database()
