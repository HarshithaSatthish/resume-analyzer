from typing import Annotated

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user_id
from app.schemas.resume import AnalyzeRequest, AnalyzeResponse
from app.services.analysis_service import analysis_service

router = APIRouter(tags=["Analysis"])


@router.post("/analyze", response_model=AnalyzeResponse, summary="Analyze an uploaded resume")
async def analyze_resume(
    payload: AnalyzeRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> AnalyzeResponse:
    return await analysis_service.analyze_upload(user_id, payload.file_id)
