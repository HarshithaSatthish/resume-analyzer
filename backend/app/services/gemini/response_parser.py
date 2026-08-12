import json
import re

from pydantic import ValidationError as PydanticValidationError

from app.middleware.error_handler import ValidationError
from app.schemas.resume import AIFeedback
from app.services.gemini.constants import MAX_FEEDBACK_LENGTH, MAX_LIST_ITEMS, MAX_SUMMARY_LENGTH
from app.utils.text_utils import sanitize_text


class GeminiResponseParser:
    LIST_FIELDS = [
        "career_suggestions",
        "resume_improvements",
        "strengths",
        "weaknesses",
        "recommended_certifications",
        "recommended_projects",
    ]

    def parse_feedback(self, content: str) -> AIFeedback:
        data = self._extract_json(content)
        normalized = self._normalize_payload(data)

        try:
            return AIFeedback(**normalized)
        except PydanticValidationError as exc:
            raise ValidationError("AI response did not match the expected feedback format.") from exc

    def _extract_json(self, content: str) -> dict:
        cleaned = content.strip()
        if not cleaned:
            raise ValidationError("Empty response from AI model.")

        if cleaned.startswith("```"):
            cleaned = re.sub(r"^```(?:json)?", "", cleaned, flags=re.IGNORECASE).strip()
            cleaned = re.sub(r"```$", "", cleaned).strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as exc:
            raise ValidationError("Failed to parse AI feedback as JSON.") from exc

        if not isinstance(data, dict):
            raise ValidationError("AI feedback response must be a JSON object.")
        return data

    def _normalize_payload(self, data: dict) -> dict:
        normalized = {
            "resume_feedback": sanitize_text(str(data.get("resume_feedback", "")), MAX_FEEDBACK_LENGTH),
            "professional_summary": sanitize_text(str(data.get("professional_summary", "")), MAX_SUMMARY_LENGTH),
        }

        for field in self.LIST_FIELDS:
            normalized[field] = self._normalize_list(data.get(field, []))

        if not normalized["resume_feedback"]:
            raise ValidationError("AI feedback response missing resume_feedback.")

        return normalized

    def _normalize_list(self, value) -> list[str]:
        if isinstance(value, str):
            items = [item.strip() for item in re.split(r"[\n;]+", value) if item.strip()]
        elif isinstance(value, list):
            items = [sanitize_text(str(item), 500) for item in value if str(item).strip()]
        else:
            items = []

        unique: list[str] = []
        seen = set()
        for item in items:
            key = item.lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(item)
        return unique[:MAX_LIST_ITEMS]


response_parser = GeminiResponseParser()
