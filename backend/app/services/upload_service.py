from pathlib import Path

from fastapi import UploadFile

from app.config import settings
from app.database.repositories import upload_repository
from app.middleware.error_handler import NotFoundError, ValidationError
from app.models.upload import UploadCreate
from app.services.resume_parser.resume_validator import resume_validator
from app.utils.file_utils import delete_file_if_exists, save_upload_file


async def save_resume_upload(user_id: str, file: UploadFile) -> dict:
    filename, file_path, size = await save_upload_file(file, settings.upload_path)

    try:
        resume_validator.validate(file_path)
    except ValidationError:
        delete_file_if_exists(file_path)
        raise

    return await upload_repository.create_upload(
        UploadCreate(
            user_id=user_id,
            filename=filename,
            original_filename=file.filename or filename,
            file_path=file_path,
            size_bytes=size,
        )
    )


async def get_upload_by_id(file_id: str, user_id: str) -> dict:
    upload = await upload_repository.find_by_id_for_user(file_id, user_id)
    if not upload:
        raise NotFoundError("Uploaded file not found.")
    return upload


def ensure_upload_file_exists(file_path: str) -> Path:
    path = Path(file_path)
    if not path.exists():
        raise NotFoundError("Uploaded file no longer exists on the server.")
    return path
