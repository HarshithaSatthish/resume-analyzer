from typing import Annotated

from fastapi import APIRouter, Depends

from app.middleware.auth import get_current_user_id
from app.schemas.resume import AIFeedbackRequest, AIFeedbackResponse
from app.services.ats import ats_service
from app.services.auth_service import get_user_gemini_api_key
from app.services.gemini import gemini_service
from app.services.resume_parser import resume_parser_service
from app.services.skill_extractor_service import skill_extractor_service
from app.services.upload_service import ensure_upload_file_exists, get_upload_by_id

router = APIRouter(tags=["Gemini AI"])


@router.post("/ai/feedback", response_model=AIFeedbackResponse, summary="Generate Gemini AI resume feedback")
async def generate_ai_feedback(
    payload: AIFeedbackRequest,
    user_id: Annotated[str, Depends(get_current_user_id)],
) -> AIFeedbackResponse:
    upload = await get_upload_by_id(payload.file_id, user_id)
    file_path = ensure_upload_file_exists(upload["file_path"])

    parsed_data = resume_parser_service.parse_pdf(str(file_path))
    detected_skills = skill_extractor_service.extract_skills(
        parsed_data.raw_text,
        resume_skills=parsed_data.skills,
    )
    ats_result = ats_service.calculate_full_result(parsed_data, detected_skills)

    user_api_key = await get_user_gemini_api_key(user_id)
    ai_feedback = gemini_service.generate_feedback(
        parsed_data,
        detected_skills,
        ats_result.scores,
        api_key=user_api_key,
        job_description=payload.job_description,
    )

    return AIFeedbackResponse(
        ai_feedback=ai_feedback,
        detected_skills=detected_skills,
        parsed_data=parsed_data,
        ats_scores=ats_result.scores,
    )
