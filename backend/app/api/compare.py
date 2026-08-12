from typing import Annotated

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user_id
from app.schemas.report import CompareRequest, CompareResponse
from app.services.analysis_service import analysis_service

router = APIRouter(tags=["Comparison"])


@router.post("/compare", response_model=CompareResponse, summary="Compare resume with job description")
async def compare_job_description(
    payload: CompareRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> CompareResponse:
    return await analysis_service.compare_report(
        user_id=user_id,
        report_id=payload.report_id,
        job_description=payload.job_description,
    )
