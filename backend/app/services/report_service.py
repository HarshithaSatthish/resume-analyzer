from pathlib import Path

from app.database.repositories import report_repository
from app.middleware.error_handler import NotFoundError
from app.models.report import ReportCreate
from app.schemas.report import HistoryResponse, JobComparisonResult, ReportDetailResponse, ReportSummary
from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData
from app.services.pdf import pdf_report_service
from app.utils.file_utils import delete_file_if_exists


class ReportService:
    async def create_report(
        self,
        user_id: str,
        upload: dict,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
        ai_feedback: AIFeedback,
        pdf_path: str,
    ) -> dict:
        title = parsed_data.name or upload.get("original_filename", "Resume Report")
        return await report_repository.create_report(
            ReportCreate(
                user_id=user_id,
                title=title,
                filename=upload["filename"],
                original_filename=upload.get("original_filename", upload["filename"]),
                file_path=upload["file_path"],
                parsed_data=parsed_data,
                detected_skills=detected_skills,
                ats_scores=ats_scores,
                ai_feedback=ai_feedback,
                pdf_path=pdf_path,
            )
        )

    async def update_job_comparison(
        self,
        report_id: str,
        user_id: str,
        comparison: JobComparisonResult,
        pdf_path: str,
    ) -> dict:
        await self.get_report_document(report_id, user_id)
        await report_repository.update_job_comparison(report_id, comparison, pdf_path)
        return await self.get_report_document(report_id, user_id)

    async def update_pdf_path(self, report_id: str, pdf_path: str) -> None:
        updated = await report_repository.update_pdf_path(report_id, pdf_path)
        if not updated:
            raise NotFoundError("Report not found.")

    async def get_history(self, user_id: str, search: str | None = None) -> HistoryResponse:
        reports = await report_repository.search_by_user(user_id, search=search)

        summaries = [
            ReportSummary(
                id=str(report["_id"]),
                title=report.get("title", "Resume Report"),
                filename=report.get("filename", ""),
                overall_score=report.get("ats_scores", {}).get("overall_score", 0.0),
                pdf_available=self._is_pdf_available(report.get("pdf_path")),
                created_at=report["created_at"].isoformat(),
                updated_at=report["updated_at"].isoformat(),
            )
            for report in reports
        ]

        return HistoryResponse(reports=summaries, total=len(summaries))

    async def get_report_detail(self, report_id: str, user_id: str) -> ReportDetailResponse:
        report = await self.get_report_document(report_id, user_id)
        job_comparison = report.get("job_comparison")

        return ReportDetailResponse(
            id=str(report["_id"]),
            title=report.get("title", "Resume Report"),
            filename=report.get("filename", ""),
            original_filename=report.get("original_filename", ""),
            parsed_data=ParsedResumeData(**report.get("parsed_data", {})),
            detected_skills=report.get("detected_skills", []),
            ats_scores=ATSScoreBreakdown(**report.get("ats_scores", {})),
            ai_feedback=AIFeedback(**report.get("ai_feedback", {})),
            job_comparison=JobComparisonResult(**job_comparison) if job_comparison else None,
            pdf_available=self._is_pdf_available(report.get("pdf_path")),
            created_at=report["created_at"].isoformat(),
            updated_at=report["updated_at"].isoformat(),
        )

    async def delete_report(self, report_id: str, user_id: str) -> None:
        report = await report_repository.delete_for_user(report_id, user_id)
        delete_file_if_exists(report.get("pdf_path"))
        delete_file_if_exists(report.get("file_path"))

    async def get_report_document(self, report_id: str, user_id: str) -> dict:
        return await report_repository.find_by_id_for_user(report_id, user_id)

    async def ensure_pdf_path(self, report_id: str, user_id: str) -> str:
        report = await self.get_report_document(report_id, user_id)
        pdf_path = report.get("pdf_path")

        if pdf_report_service.pdf_exists(pdf_path):
            return pdf_path

        job_comparison = report.get("job_comparison")
        regenerated_path = pdf_report_service.generate_report_pdf(
            report_id=report_id,
            parsed_data=ParsedResumeData(**report.get("parsed_data", {})),
            detected_skills=report.get("detected_skills", []),
            ats_scores=ATSScoreBreakdown(**report.get("ats_scores", {})),
            ai_feedback=AIFeedback(**report.get("ai_feedback", {})),
            job_comparison=JobComparisonResult(**job_comparison) if job_comparison else None,
        )
        await self.update_pdf_path(report_id, regenerated_path)
        return regenerated_path

    def _is_pdf_available(self, pdf_path: str | None) -> bool:
        return pdf_report_service.pdf_exists(pdf_path)

    async def get_user_stats(self, user_id: str) -> dict:
        total = await report_repository.count_by_user(user_id)
        avg_score = await report_repository.get_average_score(user_id)
        return {"total_reports": total, "average_score": avg_score}


report_service = ReportService()
