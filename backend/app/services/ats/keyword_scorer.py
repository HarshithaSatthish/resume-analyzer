import re

from app.services.ats.constants import ACTION_VERBS, POWER_WORDS, SECTION_KEYWORDS
from app.utils.text_utils import extract_keywords


class KeywordScorer:
    METRIC_PATTERN = re.compile(
        r"\b\d+(?:\.\d+)?%|\b\d+\+?\s*(?:years|months|users|clients|projects|team members)\b",
        re.IGNORECASE,
    )

    def score(self, text: str) -> float:
        if not text.strip():
            return 0.0

        keywords = extract_keywords(text)
        lowered = text.lower()

        section_matches = sum(1 for word in SECTION_KEYWORDS if word in keywords or word in lowered)
        section_score = (section_matches / len(SECTION_KEYWORDS)) * 35

        action_matches = sum(1 for verb in ACTION_VERBS if verb in keywords)
        action_score = min((action_matches / 6) * 30, 30)

        power_matches = sum(1 for word in POWER_WORDS if word.replace("-", " ") in lowered or word in keywords)
        power_score = min((power_matches / 4) * 20, 20)

        metric_matches = len(self.METRIC_PATTERN.findall(text))
        metric_score = min(metric_matches * 5, 15)

        total = section_score + action_score + power_score + metric_score
        return min(round(total, 2), 100.0)


keyword_scorer = KeywordScorer()
