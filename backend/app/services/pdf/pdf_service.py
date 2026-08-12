from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate

from app.config import settings
from app.schemas.report import JobComparisonResult
from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData
from app.services.pdf.chart_builder import pdf_chart_builder
from app.services.pdf.document_builder import pdf_document_builder


class PDFReportService:
    def generate_report_pdf(
        self,
        report_id: str,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
        ai_feedback: AIFeedback,
        job_comparison: JobComparisonResult | None = None,
    ) -> str:
        output_path = settings.reports_path / f"report_{report_id}.pdf"
        chart_path = settings.reports_path / f"chart_{report_id}.png"

        pdf_chart_builder.create_score_chart(ats_scores, chart_path)

        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=A4,
            rightMargin=48,
            leftMargin=48,
            topMargin=48,
            bottomMargin=56,
            title=f"Resume Report - {parsed_data.name or report_id}",
            author="AI Resume Analyzer",
        )

        story = pdf_document_builder.build_story(
            parsed_data=parsed_data,
            detected_skills=detected_skills,
            ats_scores=ats_scores,
            ai_feedback=ai_feedback,
            chart_path=str(chart_path),
            job_comparison=job_comparison,
        )

        doc.build(story, onFirstPage=self._draw_page_footer, onLaterPages=self._draw_page_footer)

        if chart_path.exists():
            chart_path.unlink()

        return str(output_path)

    def pdf_exists(self, pdf_path: str | None) -> bool:
        return bool(pdf_path and Path(pdf_path).is_file())

    def _draw_page_footer(self, canvas, doc) -> None:
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.HexColor("#94A3B8"))
        canvas.drawString(inch * 0.67, 0.45 * inch, "AI Resume Analyzer — Confidential Report")
        canvas.drawRightString(A4[0] - inch * 0.67, 0.45 * inch, f"Page {doc.page}")
        canvas.restoreState()


pdf_report_service = PDFReportService()
