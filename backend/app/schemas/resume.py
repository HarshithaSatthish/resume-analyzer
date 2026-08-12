from pydantic import BaseModel, Field, field_validator

from app.utils.text_utils import sanitize_text


class ParsedResumeData(BaseModel):
    name: str = ""
    email: str = ""
    phone: str = ""
    summary: str = ""
    education: list[str] = Field(default_factory=list)
    projects: list[str] = Field(default_factory=list)
    experience: list[str] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    certifications: list[str] = Field(default_factory=list)
    languages: list[str] = Field(default_factory=list)
    raw_text: str = ""


class ParseMetadata(BaseModel):
    page_count: int = 0
    extraction_method: str = ""
    character_count: int = 0
    line_count: int = 0
    sections_found: int = 0
    contact_fields_found: int = 0


class ParseResponse(BaseModel):
    parsed_data: ParsedResumeData
    metadata: ParseMetadata
    message: str = "Resume parsed successfully."


class ParseRequest(BaseModel):
    file_id: str = Field(..., min_length=1)

    @field_validator("file_id")
    @classmethod
    def validate_file_id(cls, value: str) -> str:
        cleaned = sanitize_text(value, max_length=128)
        if not cleaned:
            raise ValueError("file_id is required.")
        return cleaned


class UploadResponse(BaseModel):
    file_id: str
    filename: str
    original_filename: str
    size_bytes: int
    message: str = "Resume uploaded successfully."


class AnalyzeRequest(BaseModel):
    file_id: str = Field(..., min_length=1)

    @field_validator("file_id")
    @classmethod
    def validate_file_id(cls, value: str) -> str:
        cleaned = sanitize_text(value, max_length=128)
        if not cleaned:
            raise ValueError("file_id is required.")
        return cleaned


class ATSScoreBreakdown(BaseModel):
    overall_score: float
    formatting_score: float
    keyword_score: float
    skill_score: float
    project_score: float
    education_score: float
    experience_score: float
    readability_score: float
    grade: str = ""
    recommendations: list[str] = Field(default_factory=list)


class ATSScoreResponse(BaseModel):
    ats_scores: ATSScoreBreakdown
    detected_skills: list[str] = Field(default_factory=list)
    parsed_data: ParsedResumeData
    message: str = "ATS score calculated successfully."


class AIFeedback(BaseModel):
    resume_feedback: str
    career_suggestions: list[str] = Field(default_factory=list)
    resume_improvements: list[str] = Field(default_factory=list)
    professional_summary: str = ""
    strengths: list[str] = Field(default_factory=list)
    weaknesses: list[str] = Field(default_factory=list)
    recommended_certifications: list[str] = Field(default_factory=list)
    recommended_projects: list[str] = Field(default_factory=list)
    source: str = "gemini"
    model: str = ""


class AIFeedbackResponse(BaseModel):
    ai_feedback: AIFeedback
    detected_skills: list[str] = Field(default_factory=list)
    parsed_data: ParsedResumeData
    ats_scores: ATSScoreBreakdown
    message: str = "AI feedback generated successfully."


class AIFeedbackRequest(BaseModel):
    file_id: str = Field(..., min_length=1)
    job_description: str | None = Field(default=None, max_length=15000)

    @field_validator("file_id")
    @classmethod
    def validate_file_id(cls, value: str) -> str:
        cleaned = sanitize_text(value, max_length=128)
        if not cleaned:
            raise ValueError("file_id is required.")
        return cleaned

    @field_validator("job_description")
    @classmethod
    def validate_job_description(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = sanitize_text(value, max_length=15000)
        return cleaned or None


class AnalyzeResponse(BaseModel):
    report_id: str
    parsed_data: ParsedResumeData
    detected_skills: list[str]
    ats_scores: ATSScoreBreakdown
    ai_feedback: AIFeedback
    message: str = "Resume analyzed successfully."
