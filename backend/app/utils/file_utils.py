import uuid
from pathlib import Path

import aiofiles
from fastapi import HTTPException, UploadFile, status

from app.config import settings


def generate_unique_filename(original_filename: str) -> str:
    extension = Path(original_filename).suffix.lower()
    if extension != ".pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )
    return f"{uuid.uuid4().hex}{extension}"


async def validate_pdf_upload(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No file provided.",
        )

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed.",
        )

    content_type = (file.content_type or "").lower()
    if content_type and content_type not in {"application/pdf", "application/x-pdf"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are allowed.",
        )


async def save_upload_file(file: UploadFile, destination_dir: Path) -> tuple[str, str, int]:
    await validate_pdf_upload(file)

    filename = generate_unique_filename(file.filename)
    file_path = destination_dir / filename

    size = 0
    chunk_size = 1024 * 1024

    async with aiofiles.open(file_path, "wb") as output_file:
        while True:
            chunk = await file.read(chunk_size)
            if not chunk:
                break
            size += len(chunk)
            if size > settings.max_upload_size_bytes:
                await output_file.close()
                if file_path.exists():
                    file_path.unlink()
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File size exceeds the maximum limit of {settings.max_upload_size_mb}MB.",
                )
            await output_file.write(chunk)

    if size == 0:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty.",
        )

    if not _is_valid_pdf(file_path):
        file_path.unlink()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or corrupted PDF file.",
        )

    return filename, str(file_path), size


def _is_valid_pdf(file_path: Path) -> bool:
    try:
        with open(file_path, "rb") as pdf_file:
            header = pdf_file.read(5)
            return header.startswith(b"%PDF-")
    except OSError:
        return False


def delete_file_if_exists(file_path: str | None) -> None:
    if not file_path:
        return
    path = Path(file_path)
    if path.exists() and path.is_file():
        path.unlink()
