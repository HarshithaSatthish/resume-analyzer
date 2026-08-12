from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class UploadDocument(BaseModel):
    user_id: str
    filename: str
    original_filename: str
    file_path: str
    size_bytes: int = Field(..., ge=1)
    created_at: datetime


class UploadCreate(BaseModel):
    user_id: str
    filename: str
    original_filename: str
    file_path: str
    size_bytes: int


class UploadInDB(UploadDocument):
    id: str

    @classmethod
    def from_mongo(cls, document: dict[str, Any]) -> "UploadInDB":
        return cls(
            id=str(document["_id"]),
            user_id=document["user_id"],
            filename=document["filename"],
            original_filename=document["original_filename"],
            file_path=document["file_path"],
            size_bytes=document["size_bytes"],
            created_at=document["created_at"],
        )


def build_upload_document(payload: UploadCreate, created_at: datetime) -> dict[str, Any]:
    return {
        "user_id": payload.user_id,
        "filename": payload.filename,
        "original_filename": payload.original_filename,
        "file_path": payload.file_path,
        "size_bytes": payload.size_bytes,
        "created_at": created_at,
    }
