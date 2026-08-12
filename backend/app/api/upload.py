from typing import Annotated

from fastapi import APIRouter, Depends, File, UploadFile

from app.middleware.auth import get_current_user_id
from app.schemas.resume import UploadResponse
from app.services.upload_service import save_resume_upload

router = APIRouter(tags=["Upload"])


@router.post("/upload", response_model=UploadResponse, summary="Upload a resume PDF")
async def upload_resume(
    user_id: Annotated[str, Depends(get_current_user_id)],
    file: UploadFile = File(...),
) -> UploadResponse:
    upload = await save_resume_upload(user_id, file)
    return UploadResponse(
        file_id=str(upload["_id"]),
        filename=upload["filename"],
        original_filename=upload["original_filename"],
        size_bytes=upload["size_bytes"],
    )
