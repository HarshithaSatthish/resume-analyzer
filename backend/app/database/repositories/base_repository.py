from typing import Any

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from app.database.mongodb import get_database


class BaseRepository:
    collection_name: str

    @property
    def collection(self) -> AsyncIOMotorCollection:
        return get_database()[self.collection_name]

    async def find_by_id(self, document_id: ObjectId) -> dict[str, Any] | None:
        return await self.collection.find_one({"_id": document_id})

    async def insert_one(self, document: dict[str, Any]) -> ObjectId:
        result = await self.collection.insert_one(document)
        return result.inserted_id

    async def delete_by_id(self, document_id: ObjectId) -> bool:
        result = await self.collection.delete_one({"_id": document_id})
        return result.deleted_count > 0

    async def update_by_id(self, document_id: ObjectId, update: dict[str, Any]) -> bool:
        result = await self.collection.update_one({"_id": document_id}, update)
        return result.modified_count > 0 or result.matched_count > 0

    async def count(self, query: dict[str, Any] | None = None) -> int:
        return await self.collection.count_documents(query or {})
