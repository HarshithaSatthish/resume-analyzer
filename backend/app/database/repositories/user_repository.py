from typing import Any

from app.database.repositories.base_repository import BaseRepository
from app.models.collections import USERS
from app.models.user import UserCreate, build_user_document
from app.utils.object_id import parse_object_id_or_not_found
from app.utils.text_utils import utc_now


class UserRepository(BaseRepository):
    collection_name = USERS

    async def find_by_email(self, email: str) -> dict[str, Any] | None:
        return await self.collection.find_one({"email": email})

    async def create_user(self, payload: UserCreate) -> dict[str, Any]:
        now = utc_now()
        document = build_user_document(payload, created_at=now, updated_at=now)
        inserted_id = await self.insert_one(document)
        document["_id"] = inserted_id
        return document

    async def find_by_id_str(self, user_id: str) -> dict[str, Any] | None:
        object_id = parse_object_id_or_not_found(user_id, "User not found.")
        return await self.find_by_id(object_id)

    async def update_gemini_api_key(self, user_id: str, api_key: str | None) -> bool:
        object_id = parse_object_id_or_not_found(user_id, "User not found.")
        return await self.update_by_id(
            object_id,
            {"$set": {"gemini_api_key": api_key, "updated_at": utc_now()}},
        )

    async def update_profile(self, user_id: str, full_name: str) -> dict[str, Any] | None:
        object_id = parse_object_id_or_not_found(user_id, "User not found.")
        await self.update_by_id(
            object_id,
            {"$set": {"full_name": full_name, "updated_at": utc_now()}},
        )
        return await self.find_by_id(object_id)


user_repository = UserRepository()
