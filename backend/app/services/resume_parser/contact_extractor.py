import re

from app.services.resume_parser.constants import EMAIL_PATTERN, PHONE_PATTERNS, SECTION_SKIP_LINES


class ContactExtractor:
    def extract_name(self, text: str, email: str) -> str:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        if not lines:
            return ""

        for line in lines[:8]:
            normalized = line.lower().strip()
            if normalized in SECTION_SKIP_LINES:
                continue
            if self._is_contact_line(line):
                continue
            if self._looks_like_name(line):
                return self._format_name(line)

        if email:
            local_part = email.split("@")[0]
            candidate = re.sub(r"[._+\-0-9]", " ", local_part).strip()
            candidate = " ".join(candidate.split())
            if candidate and len(candidate) >= 2:
                return candidate.title()

        return self._format_name(lines[0][:60])

    def extract_email(self, text: str) -> str:
        matches = EMAIL_PATTERN.findall(text)
        if not matches:
            return ""
        preferred = [email for email in matches if not email.lower().endswith(".png")]
        return preferred[0] if preferred else matches[0]

    def extract_phone(self, text: str) -> str:
        for pattern in PHONE_PATTERNS:
            match = pattern.search(text)
            if match:
                return re.sub(r"\s+", " ", match.group(0).strip())
        return ""

    def _is_contact_line(self, line: str) -> bool:
        lowered = line.lower()
        if EMAIL_PATTERN.search(line):
            return True
        for pattern in PHONE_PATTERNS:
            if pattern.search(line):
                return True
        if any(token in lowered for token in ("linkedin", "github", "http://", "https://", "www.")):
            return True
        return False

    def _looks_like_name(self, line: str) -> bool:
        if len(line) > 60 or len(line.split()) > 5:
            return False
        if any(char.isdigit() for char in line):
            return False
        if line.isupper() and len(line.split()) <= 4:
            return True
        return bool(re.match(r"^[A-Za-z][A-Za-z\s'.-]+$", line))

    def _format_name(self, value: str) -> str:
        cleaned = " ".join(value.split())
        if cleaned.isupper() and len(cleaned) > 3:
            return cleaned.title()
        return cleaned


contact_extractor = ContactExtractor()
