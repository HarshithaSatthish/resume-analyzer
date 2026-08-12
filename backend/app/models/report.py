from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from app.schemas.report import JobComparisonResult
from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData


class ReportDocument(BaseModel):
    user_id: str
    title: str
    filename: str
    original_filename: str
    file_path: str
    parsed_data: dict[str, Any]
    detected_skills: list[str] = Field(default_factory=list)
    ats_scores: dict[str, Any]
    ai_feedback: dict[str, Any]
    job_comparison: dict[str, Any] | None = None
    pdf_path: str = ""
    created_at: datetime
    updated_at: datetime


class ReportCreate(BaseModel):
    user_id: str
    title: str
    filename: str
    original_filename: str
    file_path: str
    parsed_data: ParsedResumeData
    detected_skills: list[str]
    ats_scores: ATSScoreBreakdown
    ai_feedback: AIFeedback
    pdf_path: str = ""


class ReportInDB(ReportDocument):
    id: str

    @classmethod
    def from_mongo(cls, document: dict[str, Any]) -> "ReportInDB":
        return cls(
            id=str(document["_id"]),
            user_id=document["user_id"],
            title=document.get("title", "Resume Report"),
            filename=document.get("filename", ""),
            original_filename=document.get("original_filename", ""),
            file_path=document.get("file_path", ""),
            parsed_data=document.get("parsed_data", {}),
            detected_skills=document.get("detected_skills", []),
            ats_scores=document.get("ats_scores", {}),
            ai_feedback=document.get("ai_feedback", {}),
            job_comparison=document.get("job_comparison"),
            pdf_path=document.get("pdf_path", ""),
            created_at=document["created_at"],
            updated_at=document["updated_at"],
        )


def build_report_document(
    payload: ReportCreate,
    created_at: datetime,
    updated_at: datetime,
) -> dict[str, Any]:
    return {
        "user_id": payload.user_id,
        "title": payload.title,
        "filename": payload.filename,
        "original_filename": payload.original_filename,
        "file_path": payload.file_path,
        "parsed_data": payload.parsed_data.model_dump(),
        "detected_skills": payload.detected_skills,
        "ats_scores": payload.ats_scores.model_dump(),
        "ai_feedback": payload.ai_feedback.model_dump(),
        "job_comparison": None,
        "pdf_path": payload.pdf_path,
        "created_at": created_at,
        "updated_at": updated_at,
    }


def build_job_comparison_update(
    comparison: JobComparisonResult,
    pdf_path: str,
    updated_at: datetime,
) -> dict[str, Any]:
    return {
        "job_comparison": comparison.model_dump(),
        "pdf_path": pdf_path,
        "updated_at": updated_at,
    }
