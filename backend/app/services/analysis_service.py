from app.schemas.report import CompareResponse
from app.schemas.resume import AnalyzeResponse, ParsedResumeData
from app.services.ats import ats_service
from app.services.auth_service import get_user_gemini_api_key
from app.services.comparison_service import comparison_service
from app.services.gemini import gemini_service
from app.services.pdf import pdf_report_service
from app.services.report_service import report_service
from app.services.resume_parser import resume_parser_service
from app.services.skill_extractor_service import skill_extractor_service
from app.services.upload_service import ensure_upload_file_exists, get_upload_by_id


class AnalysisService:
    async def analyze_upload(self, user_id: str, file_id: str) -> AnalyzeResponse:
        upload = await get_upload_by_id(file_id, user_id)
        file_path = ensure_upload_file_exists(upload["file_path"])

        parsed_data = resume_parser_service.parse_pdf(str(file_path))
        detected_skills = skill_extractor_service.extract_skills(
            parsed_data.raw_text,
            resume_skills=parsed_data.skills,
        )
        ats_scores = ats_service.calculate_scores(parsed_data, detected_skills)

        user_api_key = await get_user_gemini_api_key(user_id)
        ai_feedback = gemini_service.generate_feedback(
            parsed_data,
            detected_skills,
            ats_scores,
            api_key=user_api_key,
        )

        report = await report_service.create_report(
            user_id=user_id,
            upload=upload,
            parsed_data=parsed_data,
            detected_skills=detected_skills,
            ats_scores=ats_scores,
            ai_feedback=ai_feedback,
            pdf_path="",
        )

        report_id = str(report["_id"])
        pdf_path = pdf_report_service.generate_report_pdf(
            report_id=report_id,
            parsed_data=parsed_data,
            detected_skills=detected_skills,
            ats_scores=ats_scores,
            ai_feedback=ai_feedback,
        )

        await report_service.update_pdf_path(report_id, pdf_path)

        return AnalyzeResponse(
            report_id=report_id,
            parsed_data=parsed_data,
            detected_skills=detected_skills,
            ats_scores=ats_scores,
            ai_feedback=ai_feedback,
        )

    async def compare_report(
        self,
        user_id: str,
        report_id: str,
        job_description: str,
    ) -> CompareResponse:
        report = await report_service.get_report_document(report_id, user_id)
        parsed_data = ParsedResumeData(**report.get("parsed_data", {}))
        detected_skills = report.get("detected_skills", [])

        comparison = comparison_service.compare_with_job_description(
            resume_text=parsed_data.raw_text,
            detected_skills=detected_skills,
            job_description=job_description,
        )

        from app.schemas.resume import AIFeedback, ATSScoreBreakdown

        pdf_path = pdf_report_service.generate_report_pdf(
            report_id=report_id,
            parsed_data=parsed_data,
            detected_skills=detected_skills,
            ats_scores=ATSScoreBreakdown(**report.get("ats_scores", {})),
            ai_feedback=AIFeedback(**report.get("ai_feedback", {})),
            job_comparison=comparison,
        )

        await report_service.update_job_comparison(report_id, user_id, comparison, pdf_path)

        return CompareResponse(report_id=report_id, comparison=comparison)


analysis_service = AnalysisService()
