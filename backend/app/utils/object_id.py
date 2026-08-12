from bson import ObjectId
from bson.errors import InvalidId

from app.middleware.error_handler import NotFoundError, ValidationError


def parse_object_id(value: str, error_message: str = "Invalid identifier.") -> ObjectId:
    try:
        return ObjectId(value)
    except InvalidId as exc:
        raise ValidationError(error_message) from exc


def parse_object_id_or_not_found(value: str, error_message: str = "Resource not found.") -> ObjectId:
    try:
        return ObjectId(value)
    except InvalidId as exc:
        raise NotFoundError(error_message) from exc


def stringify_object_id(value: ObjectId | str | None) -> str | None:
    if value is None:
        return None
    return str(value)
