from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.schemas.resume import ATSScoreBreakdown
from app.services.pdf.constants import CHART_COLORS, SCORE_METRICS


class PDFChartBuilder:
    def create_score_chart(self, ats_scores: ATSScoreBreakdown, chart_path: Path) -> None:
        labels = [label for _, label, _ in SCORE_METRICS]
        values = [getattr(ats_scores, key) for key, _, _ in SCORE_METRICS]

        figure, axis = plt.subplots(figsize=(8, 4))
        bars = axis.bar(labels, values, color=CHART_COLORS)
        axis.set_ylim(0, 100)
        axis.set_ylabel("Score")
        grade_label = f" | Grade: {ats_scores.grade}" if ats_scores.grade else ""
        axis.set_title(f"ATS Breakdown (Overall: {round(ats_scores.overall_score)}%{grade_label}")
        axis.bar_label(bars, fmt="%.0f", padding=3, fontsize=9)
        plt.xticks(rotation=25, ha="right")
        figure.tight_layout()
        figure.savefig(chart_path, dpi=150, bbox_inches="tight")
        plt.close(figure)


pdf_chart_builder = PDFChartBuilder()
