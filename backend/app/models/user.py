from datetime import datetime
from typing import Any

from pydantic import BaseModel, EmailStr, Field


class UserDocument(BaseModel):
    full_name: str
    email: EmailStr
    hashed_password: str
    gemini_api_key: str | None = None
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    hashed_password: str


class UserInDB(UserDocument):
    id: str

    @classmethod
    def from_mongo(cls, document: dict[str, Any]) -> "UserInDB":
        return cls(
            id=str(document["_id"]),
            full_name=document["full_name"],
            email=document["email"],
            hashed_password=document["hashed_password"],
            gemini_api_key=document.get("gemini_api_key"),
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )


def build_user_document(payload: UserCreate, created_at: datetime, updated_at: datetime) -> dict[str, Any]:
    return {
        "full_name": payload.full_name,
        "email": payload.email,
        "hashed_password": payload.hashed_password,
        "gemini_api_key": None,
        "created_at": created_at,
        "updated_at": updated_at,
    }
