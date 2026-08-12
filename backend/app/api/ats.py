from typing import Annotated

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user_id
from app.schemas.resume import ATSScoreResponse, ParseRequest
from app.services.ats import ats_service
from app.services.resume_parser import resume_parser_service
from app.services.skill_extractor_service import skill_extractor_service
from app.services.upload_service import ensure_upload_file_exists, get_upload_by_id

router = APIRouter(tags=["ATS Scoring"])


@router.post("/ats", response_model=ATSScoreResponse, summary="Calculate ATS score for an uploaded resume")
async def calculate_ats_score(
    payload: ParseRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> ATSScoreResponse:
    upload = await get_upload_by_id(payload.file_id, user_id)
    file_path = ensure_upload_file_exists(upload["file_path"])

    parsed_data = resume_parser_service.parse_pdf(str(file_path))
    detected_skills = skill_extractor_service.extract_skills(
        parsed_data.raw_text,
        resume_skills=parsed_data.skills,
    )
    result = ats_service.calculate_full_result(parsed_data, detected_skills)

    return ATSScoreResponse(
        ats_scores=result.scores,
        detected_skills=detected_skills,
        parsed_data=parsed_data,
    )
