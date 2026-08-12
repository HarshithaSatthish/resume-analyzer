import logging

import google.generativeai as genai

from app.config import settings
from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData
from app.services.gemini.constants import GEMINI_SYSTEM_INSTRUCTION, GENERATION_CONFIG
from app.services.gemini.fallback_generator import fallback_generator
from app.services.gemini.prompt_builder import prompt_builder
from app.services.gemini.response_parser import response_parser

logger = logging.getLogger(__name__)


class GeminiClient:
    def generate_feedback(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
        api_key: str | None = None,
        job_description: str | None = None,
    ) -> AIFeedback:
        key = (api_key or settings.gemini_api_key or "").strip()
        if not key:
            logger.info("No Gemini API key configured. Using fallback feedback generator.")
            return fallback_generator.generate(parsed_data, detected_skills, ats_scores)

        try:
            genai.configure(api_key=key)
            model = genai.GenerativeModel(
                model_name=settings.gemini_model,
                system_instruction=GEMINI_SYSTEM_INSTRUCTION,
            )

            prompt = prompt_builder.build_feedback_prompt(
                parsed_data,
                detected_skills,
                ats_scores,
                job_description=job_description,
            )

            response = model.generate_content(
                prompt,
                generation_config=GENERATION_CONFIG,
            )

            content = getattr(response, "text", None) or self._extract_text_from_parts(response)
            feedback = response_parser.parse_feedback(content)
            return feedback.model_copy(
                update={
                    "source": "gemini",
                    "model": settings.gemini_model,
                }
            )
        except Exception as exc:
            logger.warning("Gemini API call failed: %s. Using fallback feedback.", exc)
            fallback = fallback_generator.generate(parsed_data, detected_skills, ats_scores)
            return fallback.model_copy(
                update={
                    "source": "fallback",
                    "model": f"fallback-after-error:{settings.gemini_model}",
                }
            )

    def _extract_text_from_parts(self, response) -> str:
        if not response or not getattr(response, "candidates", None):
            return ""
        parts = response.candidates[0].content.parts
        return "".join(getattr(part, "text", "") for part in parts)


gemini_client = GeminiClient()
