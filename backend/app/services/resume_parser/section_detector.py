import re

from app.services.resume_parser.constants import SECTION_HEADERS


class SectionDetector:
    def detect_section(self, line: str) -> str | None:
        normalized = self._normalize_header(line)
        if not normalized:
            return None

        for section, headers in SECTION_HEADERS.items():
            for header in headers:
                if normalized == header:
                    return self._map_section(section)
                if normalized.startswith(header) and len(normalized) <= len(header) + 15:
                    return self._map_section(section)

        if re.match(r"^(experience|education|projects|skills|certifications|languages)\b", normalized):
            return self._map_section(normalized.split()[0])

        return None

    def _normalize_header(self, line: str) -> str:
        cleaned = line.strip().strip(":").strip("*#_ ").lower()
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned

    def _map_section(self, section: str) -> str:
        mapping = {
            "summary": "summary",
            "experience": "experience",
            "internship": "experience",
            "internships": "experience",
            "education": "education",
            "projects": "projects",
            "skills": "skills",
            "certifications": "certifications",
            "languages": "languages",
        }
        return mapping.get(section, section)


section_detector = SectionDetector()
