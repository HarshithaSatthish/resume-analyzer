import re
from datetime import datetime, timezone


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def sanitize_text(value: str, max_length: int = 10000) -> str:
    cleaned = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", value or "")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    return cleaned[:max_length]


def sanitize_email(email: str) -> str:
    return sanitize_text(email, max_length=254).lower()


def normalize_skill(skill: str) -> str:
    return re.sub(r"\s+", " ", skill.strip())


def extract_keywords(text: str, min_length: int = 3) -> set[str]:
    words = re.findall(r"[A-Za-z][A-Za-z0-9+#./-]*", text.lower())
    return {word for word in words if len(word) >= min_length}


def calculate_readability_score(text: str) -> float:
    if not text.strip():
        return 0.0

    sentences = max(len(re.findall(r"[.!?]+", text)), 1)
    words = re.findall(r"\b\w+\b", text)
    word_count = max(len(words), 1)
    avg_sentence_length = word_count / sentences

    if 12 <= avg_sentence_length <= 22:
        base = 90.0
    elif 8 <= avg_sentence_length <= 28:
        base = 75.0
    else:
        base = 55.0

    unique_ratio = len(set(word.lower() for word in words)) / word_count
    diversity_bonus = min(unique_ratio * 20, 10)
    return min(round(base + diversity_bonus, 2), 100.0)
