import re

from app.services.resume_parser.constants import (
    BULLET_PREFIX_PATTERN,
    DATE_RANGE_PATTERN,
    MAX_SECTION_ITEMS,
    MAX_SKILL_ITEMS,
    SKILL_DELIMITERS,
)
from app.services.resume_parser.section_detector import section_detector


class SectionParser:
    def parse_sections(self, text: str) -> dict[str, list[str]]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        buckets: dict[str, list[str]] = {
            "summary": [],
            "education": [],
            "experience": [],
            "projects": [],
            "skills": [],
            "certifications": [],
            "languages": [],
        }

        current_section: str | None = None

        for line in lines:
            detected = section_detector.detect_section(line)
            if detected:
                current_section = detected
                continue

            if current_section:
                buckets[current_section].append(line)

        return {
            "education": self._parse_block_items(buckets["education"]),
            "experience": self._parse_block_items(buckets["experience"], merge_dates=True),
            "projects": self._parse_block_items(buckets["projects"]),
            "skills": self._parse_skills(buckets["skills"]),
            "certifications": self._parse_block_items(buckets["certifications"]),
            "languages": self._parse_languages(buckets["languages"]),
            "summary": self._parse_block_items(buckets["summary"], max_items=5),
        }

    def _parse_block_items(
        self,
        lines: list[str],
        merge_dates: bool = False,
        max_items: int = MAX_SECTION_ITEMS,
    ) -> list[str]:
        if not lines:
            return []

        items: list[str] = []
        buffer: list[str] = []

        for line in lines:
            is_bullet = bool(BULLET_PREFIX_PATTERN.match(line))
            cleaned_line = BULLET_PREFIX_PATTERN.sub("", line).strip()

            if is_bullet:
                if buffer:
                    items.append(self._join_buffer(buffer))
                    buffer = []
                items.append(cleaned_line)
                continue

            if merge_dates and DATE_RANGE_PATTERN.search(line) and buffer:
                items.append(self._join_buffer(buffer))
                buffer = [cleaned_line]
                continue

            if len(cleaned_line) < 100 and cleaned_line.endswith(":") and buffer:
                items.append(self._join_buffer(buffer))
                buffer = [cleaned_line.rstrip(":")]
                continue

            buffer.append(cleaned_line)

        if buffer:
            items.append(self._join_buffer(buffer))

        return self._deduplicate(items, max_items)

    def _parse_skills(self, lines: list[str]) -> list[str]:
        if not lines:
            return []

        combined = " ".join(BULLET_PREFIX_PATTERN.sub("", line) for line in lines)
        tokens = SKILL_DELIMITERS.split(combined)
        skills: list[str] = []

        for token in tokens:
            cleaned = token.strip(" .-•*")
            if not cleaned or len(cleaned) < 2:
                continue
            if len(cleaned) > 50:
                continue
            if cleaned.lower() in {"and", "or", "etc", "including"}:
                continue
            skills.append(cleaned)

        if not skills and lines:
            return self._parse_block_items(lines, max_items=MAX_SKILL_ITEMS)

        return self._deduplicate(skills, MAX_SKILL_ITEMS)

    def _parse_languages(self, lines: list[str]) -> list[str]:
        languages = self._parse_skills(lines)
        if languages:
            return languages
        return self._parse_block_items(lines, max_items=10)

    def _join_buffer(self, buffer: list[str]) -> str:
        return re.sub(r"\s+", " ", " ".join(buffer)).strip()

    def _deduplicate(self, items: list[str], limit: int) -> list[str]:
        unique: list[str] = []
        seen: set[str] = set()
        for item in items:
            key = item.lower()
            if key and key not in seen:
                seen.add(key)
                unique.append(item)
        return unique[:limit]


section_parser = SectionParser()
