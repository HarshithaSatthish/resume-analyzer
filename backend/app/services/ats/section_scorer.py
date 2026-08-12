import re

from app.services.ats.constants import IDEAL_SECTION_COUNTS

DATE_PATTERN = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}\b",
    re.IGNORECASE,
)


class SectionScorer:
    def score_experience(self, items: list[str]) -> float:
        return self._score_items(items, ideal_count=IDEAL_SECTION_COUNTS["experience"], depth_weight=0.35)

    def score_education(self, items: list[str]) -> float:
        return self._score_items(items, ideal_count=IDEAL_SECTION_COUNTS["education"], depth_weight=0.25)

    def score_projects(self, items: list[str]) -> float:
        return self._score_items(items, ideal_count=IDEAL_SECTION_COUNTS["projects"], depth_weight=0.30)

    def _score_items(self, items: list[str], ideal_count: int, depth_weight: float) -> float:
        count = len(items)
        if count == 0:
            return 20.0

        count_score = self._count_score(count, ideal_count)
        depth_score = self._depth_score(items)
        date_score = self._date_score(items)

        combined = count_score * (1 - depth_weight) + depth_score * depth_weight * 0.7 + date_score * 0.3
        return min(round(combined, 2), 100.0)

    def _count_score(self, count: int, ideal: int) -> float:
        if count == 1:
            return 50.0
        if count < ideal:
            return 70.0
        if count <= ideal + 2:
            return 92.0
        return 100.0

    def _depth_score(self, items: list[str]) -> float:
        if not items:
            return 0.0
        avg_length = sum(len(item) for item in items) / len(items)
        if avg_length >= 120:
            return 95.0
        if avg_length >= 70:
            return 80.0
        if avg_length >= 40:
            return 65.0
        return 45.0

    def _date_score(self, items: list[str]) -> float:
        if not items:
            return 0.0
        dated_items = sum(1 for item in items if DATE_PATTERN.search(item))
        ratio = dated_items / len(items)
        return min(ratio * 100, 100.0)


section_scorer = SectionScorer()
