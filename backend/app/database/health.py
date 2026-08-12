from app.database.mongodb import check_database_connection, ping_database


async def get_database_health() -> dict:
    is_connected, detail = await check_database_connection()

    if not is_connected:
        return {
            "status": "disconnected",
            "connected": False,
            "detail": detail,
        }

    stats = await ping_database()
    return {
        "status": "connected",
        "connected": True,
        "detail": detail,
        "database": stats.get("database"),
        "collections": stats.get("collections", 0),
        "documents": stats.get("objects", 0),
    }
