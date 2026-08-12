from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData
from app.services.gemini.client import gemini_client


class GeminiService:
    def generate_feedback(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
        api_key: str | None = None,
        job_description: str | None = None,
    ) -> AIFeedback:
        return gemini_client.generate_feedback(
            parsed_data=parsed_data,
            detected_skills=detected_skills,
            ats_scores=ats_scores,
            api_key=api_key,
            job_description=job_description,
        )


gemini_service = GeminiService()
