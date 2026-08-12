from typing import Annotated

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user_id
from app.schemas.resume import ParseRequest, ParseResponse
from app.services.resume_parser import resume_parser_service
from app.services.upload_service import ensure_upload_file_exists, get_upload_by_id

router = APIRouter(tags=["Resume Parser"])


@router.post("/parse", response_model=ParseResponse, summary="Parse an uploaded resume PDF")
async def parse_resume(
    payload: ParseRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> ParseResponse:
    upload = await get_upload_by_id(payload.file_id, user_id)
    file_path = ensure_upload_file_exists(upload["file_path"])
    return resume_parser_service.parse_pdf_with_metadata(str(file_path))
