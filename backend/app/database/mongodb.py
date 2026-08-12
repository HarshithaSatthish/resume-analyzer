import logging
from typing import Any

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

from app.config import settings

logger = logging.getLogger(__name__)

client: AsyncIOMotorClient | None = None
database: AsyncIOMotorDatabase | None = None


async def connect_to_mongodb() -> None:
    global client, database

    client = AsyncIOMotorClient(
        settings.mongodb_url,
        maxPoolSize=settings.mongodb_max_pool_size,
        minPoolSize=settings.mongodb_min_pool_size,
        serverSelectionTimeoutMS=settings.mongodb_server_selection_timeout_ms,
        connectTimeoutMS=settings.mongodb_connect_timeout_ms,
    )
    database = client[settings.database_name]

    await database.command("ping")
    logger.info("Connected to MongoDB database: %s", settings.database_name)


async def close_mongodb_connection() -> None:
    global client, database
    if client is not None:
        client.close()
        logger.info("MongoDB connection closed.")
    client = None
    database = None


def get_database() -> AsyncIOMotorDatabase:
    if database is None:
        raise RuntimeError("Database connection is not initialized.")
    return database


def get_client() -> AsyncIOMotorClient:
    if client is None:
        raise RuntimeError("Database client is not initialized.")
    return client


async def ping_database() -> dict[str, Any]:
    db = get_database()
    result = await db.command("ping")
    stats = await db.command("dbStats")
    return {
        "ok": result.get("ok", 0) == 1,
        "database": settings.database_name,
        "collections": stats.get("collections", 0),
        "objects": stats.get("objects", 0),
        "storage_size": stats.get("storageSize", 0),
    }


async def check_database_connection() -> tuple[bool, str]:
    try:
        ping_result = await ping_database()
        if ping_result["ok"]:
            return True, "connected"
        return False, "ping_failed"
    except (ConnectionFailure, ServerSelectionTimeoutError, RuntimeError) as exc:
        logger.warning("Database health check failed: %s", exc)
        return False, str(exc)
