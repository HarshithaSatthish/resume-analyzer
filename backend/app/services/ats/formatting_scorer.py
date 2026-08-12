import re

from app.schemas.resume import ParsedResumeData


class FormattingScorer:
    def score(self, parsed_data: ParsedResumeData) -> float:
        points = 0.0
        max_points = 100.0

        if parsed_data.name:
            points += 12
        if parsed_data.email:
            points += 12
        if parsed_data.phone:
            points += 8
        if parsed_data.summary:
            points += 10
        if parsed_data.experience:
            points += 18
        if parsed_data.education:
            points += 12
        if parsed_data.skills:
            points += 10
        if parsed_data.projects:
            points += 8
        if parsed_data.certifications:
            points += 5
        if parsed_data.languages:
            points += 5

        structure_bonus = self._structure_bonus(parsed_data.raw_text)
        points += structure_bonus

        return min(round(points, 2), max_points)

    def _structure_bonus(self, text: str) -> float:
        if not text.strip():
            return 0.0

        bonus = 0.0
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        bullet_lines = sum(
            1 for line in lines if re.match(r"^[\u2022\u2023\u25E6\u2043\u2219\-*●○◦▪▫]", line)
        )
        if bullet_lines >= 3:
            bonus += 5
        if bullet_lines >= 8:
            bonus += 3

        if 400 <= len(text) <= 8000:
            bonus += 4
        elif len(text) > 200:
            bonus += 2

        if len(lines) >= 15:
            bonus += 3

        return min(bonus, 10.0)


formatting_scorer = FormattingScorer()
