from typing import Any

from app.database.repositories.base_repository import BaseRepository
from app.models.collections import UPLOADS
from app.models.upload import UploadCreate, build_upload_document
from app.utils.object_id import parse_object_id_or_not_found
from app.utils.text_utils import utc_now


class UploadRepository(BaseRepository):
    collection_name = UPLOADS

    async def create_upload(self, payload: UploadCreate) -> dict[str, Any]:
        document = build_upload_document(payload, created_at=utc_now())
        inserted_id = await self.insert_one(document)
        document["_id"] = inserted_id
        return document

    async def find_by_id_for_user(self, file_id: str, user_id: str) -> dict[str, Any] | None:
        object_id = parse_object_id_or_not_found(file_id, "Uploaded file not found.")
        return await self.collection.find_one({"_id": object_id, "user_id": user_id})

    async def list_by_user(self, user_id: str, limit: int = 50) -> list[dict[str, Any]]:
        cursor = self.collection.find({"user_id": user_id}).sort("created_at", -1).limit(limit)
        return await cursor.to_list(length=limit)


upload_repository = UploadRepository()
