GEMINI_SYSTEM_INSTRUCTION = (
    "You are an expert resume coach, career advisor, and ATS optimization specialist. "
    "Provide actionable, professional, and honest feedback. "
    "Always respond with valid JSON matching the requested schema exactly."
)

FEEDBACK_JSON_SCHEMA = {
    "resume_feedback": "string",
    "career_suggestions": ["string"],
    "resume_improvements": ["string"],
    "professional_summary": "string",
    "strengths": ["string"],
    "weaknesses": ["string"],
    "recommended_certifications": ["string"],
    "recommended_projects": ["string"],
}

GENERATION_CONFIG = {
    "temperature": 0.65,
    "top_p": 0.9,
    "top_k": 40,
    "max_output_tokens": 2048,
    "response_mime_type": "application/json",
}

MAX_LIST_ITEMS = 6
MAX_FEEDBACK_LENGTH = 2000
MAX_SUMMARY_LENGTH = 600
