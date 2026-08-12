from datetime import datetime, timezone
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Image, Paragraph, Spacer, Table, TableStyle

from app.schemas.report import JobComparisonResult
from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData
from app.services.pdf.constants import (
    BRAND_DARK,
    BRAND_PRIMARY,
    PARSED_SECTIONS,
    SCORE_METRICS,
    TABLE_GRID,
    TABLE_HEADER_BG,
    TABLE_ROW_ALT,
)


class PDFDocumentBuilder:
    def __init__(self) -> None:
        styles = getSampleStyleSheet()
        self.title_style = ParagraphStyle(
            "PdfTitle",
            parent=styles["Heading1"],
            fontSize=22,
            textColor=BRAND_PRIMARY,
            spaceAfter=16,
        )
        self.heading_style = ParagraphStyle(
            "PdfHeading",
            parent=styles["Heading2"],
            fontSize=14,
            textColor=BRAND_DARK,
            spaceBefore=12,
            spaceAfter=8,
        )
        self.body_style = ParagraphStyle(
            "PdfBody",
            parent=styles["BodyText"],
            fontSize=10,
            leading=14,
        )
        self.small_style = ParagraphStyle(
            "PdfSmall",
            parent=styles["BodyText"],
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#64748B"),
        )

    def build_story(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
        ai_feedback: AIFeedback,
        chart_path: str,
        job_comparison: JobComparisonResult | None = None,
    ) -> list:
        generated_at = datetime.now(timezone.utc).strftime("%B %d, %Y at %H:%M UTC")
        story: list = [
            Paragraph("AI Resume Analyzer Report", self.title_style),
            Paragraph(
                f"<b>Candidate:</b> {self._text(parsed_data.name or 'Not detected')}<br/>"
                f"<b>Email:</b> {self._text(parsed_data.email or 'Not detected')}<br/>"
                f"<b>Phone:</b> {self._text(parsed_data.phone or 'Not detected')}<br/>"
                f"<b>Generated:</b> {generated_at}",
                self.body_style,
            ),
            Spacer(1, 0.2 * inch),
            Paragraph("ATS Score Summary", self.heading_style),
            self._build_score_table(ats_scores),
            Spacer(1, 0.15 * inch),
            Image(chart_path, width=5.5 * inch, height=3 * inch),
        ]

        if ats_scores.recommendations:
            story.extend(
                [
                    Paragraph("ATS Recommendations", self.heading_style),
                    Paragraph(self._format_list(ats_scores.recommendations), self.body_style),
                ]
            )

        story.extend(self._build_parsed_sections(parsed_data))
        story.extend(
            [
                Paragraph("Detected Skills", self.heading_style),
                Paragraph(self._text(", ".join(detected_skills) or "No skills detected."), self.body_style),
            ]
        )

        if job_comparison:
            story.extend(self._build_job_comparison(job_comparison))

        story.extend(self._build_ai_feedback(ai_feedback))
        return story

    def _build_parsed_sections(self, parsed_data: ParsedResumeData) -> list:
        blocks: list = []
        for field, title in PARSED_SECTIONS:
            value = getattr(parsed_data, field)
            if isinstance(value, str) and value.strip():
                blocks.extend(
                    [
                        Paragraph(title, self.heading_style),
                        Paragraph(self._text(value), self.body_style),
                    ]
                )
            elif isinstance(value, list) and value:
                blocks.extend(
                    [
                        Paragraph(title, self.heading_style),
                        Paragraph(self._format_list(value), self.body_style),
                    ]
                )
        return blocks

    def _build_job_comparison(self, comparison: JobComparisonResult) -> list:
        return [
            Paragraph("Job Description Comparison", self.heading_style),
            Paragraph(
                f"<b>Match Percentage:</b> {round(comparison.match_percentage)}%",
                self.body_style,
            ),
            Paragraph(
                "<b>Matched Skills:</b> "
                + self._text(", ".join(comparison.matched_skills) or "None"),
                self.body_style,
            ),
            Paragraph(
                "<b>Missing Skills:</b> "
                + self._text(", ".join(comparison.missing_skills) or "None"),
                self.body_style,
            ),
        ]

    def _build_ai_feedback(self, ai_feedback: AIFeedback) -> list:
        return [
            Paragraph("AI Feedback", self.heading_style),
            Paragraph(self._text(ai_feedback.resume_feedback), self.body_style),
            Paragraph("Strengths", self.heading_style),
            Paragraph(self._format_list(ai_feedback.strengths), self.body_style),
            Paragraph("Weaknesses", self.heading_style),
            Paragraph(self._format_list(ai_feedback.weaknesses), self.body_style),
            Paragraph("Recommended Improvements", self.heading_style),
            Paragraph(self._format_list(ai_feedback.resume_improvements), self.body_style),
            Paragraph("Career Suggestions", self.heading_style),
            Paragraph(self._format_list(ai_feedback.career_suggestions), self.body_style),
        ]

    def _build_score_table(self, ats_scores: ATSScoreBreakdown) -> Table:
        data = [["Metric", "Weight", "Score"]]
        data.append(["Overall", "100%", f"{round(ats_scores.overall_score)}%"])
        if ats_scores.grade:
            data.append(["Grade", "—", ats_scores.grade])

        for key, label, weight in SCORE_METRICS:
            data.append([label, weight, f"{round(getattr(ats_scores, key))}%"])

        table = Table(data, colWidths=[2.5 * inch, 1.2 * inch, 1.3 * inch])
        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), TABLE_HEADER_BG),
                    ("TEXTCOLOR", (0, 0), (-1, 0), BRAND_DARK),
                    ("GRID", (0, 0), (-1, -1), 0.5, TABLE_GRID),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("ALIGN", (1, 1), (-1, -1), "CENTER"),
                    ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, TABLE_ROW_ALT]),
                ]
            )
        )
        return table

    def _text(self, value: str) -> str:
        return escape(value or "")

    def _format_list(self, items: list[str]) -> str:
        if not items:
            return "None"
        return "<br/>".join(f"• {self._text(item)}" for item in items)


pdf_document_builder = PDFDocumentBuilder()
