from pydantic import BaseModel, Field, field_validator

from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData
from app.utils.text_utils import sanitize_text


class CompareRequest(BaseModel):
    report_id: str = Field(..., min_length=1)
    job_description: str = Field(..., min_length=20, max_length=15000)

    @field_validator("report_id")
    @classmethod
    def validate_report_id(cls, value: str) -> str:
        cleaned = sanitize_text(value, max_length=128)
        if not cleaned:
            raise ValueError("report_id is required.")
        return cleaned

    @field_validator("job_description")
    @classmethod
    def validate_job_description(cls, value: str) -> str:
        cleaned = sanitize_text(value, max_length=15000)
        if len(cleaned) < 20:
            raise ValueError("Job description must be at least 20 characters long.")
        return cleaned


class JobComparisonResult(BaseModel):
    match_percentage: float
    matched_skills: list[str] = Field(default_factory=list)
    missing_skills: list[str] = Field(default_factory=list)
    job_keywords: list[str] = Field(default_factory=list)


class CompareResponse(BaseModel):
    report_id: str
    comparison: JobComparisonResult
    message: str = "Job description comparison completed."


class ReportSummary(BaseModel):
    id: str
    title: str
    filename: str
    overall_score: float
    pdf_available: bool = False
    created_at: str
    updated_at: str


class HistoryResponse(BaseModel):
    reports: list[ReportSummary]
    total: int


class ReportDetailResponse(BaseModel):
    id: str
    title: str
    filename: str
    original_filename: str
    parsed_data: ParsedResumeData
    detected_skills: list[str]
    ats_scores: ATSScoreBreakdown
    ai_feedback: AIFeedback
    job_comparison: JobComparisonResult | None = None
    pdf_available: bool
    created_at: str
    updated_at: str


class DeleteReportResponse(BaseModel):
    message: str
    report_id: str
