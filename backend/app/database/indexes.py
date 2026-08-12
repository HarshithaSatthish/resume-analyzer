import logging

from app.database.mongodb import get_database
from app.models.collections import REPORTS, UPLOADS, USERS

logger = logging.getLogger(__name__)

INDEX_DEFINITIONS: dict[str, list] = {
    USERS: [
        {"keys": [("email", 1)], "options": {"unique": True, "name": "users_email_unique"}},
        {"keys": [("created_at", -1)], "options": {"name": "users_created_at_desc"}},
    ],
    UPLOADS: [
        {
            "keys": [("user_id", 1), ("created_at", -1)],
            "options": {"name": "uploads_user_created_desc"},
        },
        {
            "keys": [("filename", 1)],
            "options": {"name": "uploads_filename"},
        },
    ],
    REPORTS: [
        {
            "keys": [("user_id", 1), ("created_at", -1)],
            "options": {"name": "reports_user_created_desc"},
        },
        {
            "keys": [("title", "text"), ("original_filename", "text")],
            "options": {"name": "reports_text_search"},
        },
        {
            "keys": [("user_id", 1), ("title", 1)],
            "options": {"name": "reports_user_title"},
        },
        {
            "keys": [("ats_scores.overall_score", -1)],
            "options": {"name": "reports_overall_score_desc"},
        },
    ],
}


async def ensure_indexes() -> None:
    database = get_database()

    for collection_name, indexes in INDEX_DEFINITIONS.items():
        collection = database[collection_name]
        for index in indexes:
            await collection.create_index(index["keys"], **index["options"])
            logger.info("Ensured index %s on %s", index["options"].get("name"), collection_name)

    logger.info("All MongoDB indexes verified.")
