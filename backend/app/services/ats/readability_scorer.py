import re

from app.utils.text_utils import calculate_readability_score


class ReadabilityScorer:
    def score(self, text: str) -> float:
        if not text.strip():
            return 0.0

        base = calculate_readability_score(text)
        bullet_bonus = self._bullet_bonus(text)
        jargon_penalty = self._jargon_penalty(text)

        adjusted = base + bullet_bonus - jargon_penalty
        return min(max(round(adjusted, 2), 0.0), 100.0)

    def _bullet_bonus(self, text: str) -> float:
        bullets = len(re.findall(r"^[\u2022\u2023\u25E6\u2043\u2219\-*●]", text, re.MULTILINE))
        return min(bullets * 0.5, 5.0)

    def _jargon_penalty(self, text: str) -> float:
        words = re.findall(r"\b\w+\b", text.lower())
        if not words:
            return 0.0
        long_words = sum(1 for word in words if len(word) > 14)
        ratio = long_words / len(words)
        return min(ratio * 30, 8.0)


readability_scorer = ReadabilityScorer()
