import re
from dataclasses import dataclass, field

from app.middleware.error_handler import ValidationError
from app.services.resume_parser.constants import DATE_RANGE_PATTERN, EMAIL_PATTERN
from app.services.resume_parser.contact_extractor import contact_extractor
from app.services.resume_parser.pdf_text_extractor import pdf_text_extractor
from app.services.resume_parser.section_parser import section_parser
from app.utils.text_utils import sanitize_text

# High-confidence non-resume document signals (need multiple to reject)
STRONG_NON_RESUME_PATTERNS = [
    re.compile(r"\btax invoice\b", re.IGNORECASE),
    re.compile(r"\bbill to\s*:", re.IGNORECASE),
    re.compile(r"\bship to\s*:", re.IGNORECASE),
    re.compile(r"\bamount due\b", re.IGNORECASE),
    re.compile(r"\bpayment due\b", re.IGNORECASE),
    re.compile(r"\bbank statement\b", re.IGNORECASE),
    re.compile(r"\baccount statement\b", re.IGNORECASE),
    re.compile(r"\btable of contents\b", re.IGNORECASE),
    re.compile(r"\bnutrition facts\b", re.IGNORECASE),
    re.compile(r"\bingredients\s*:", re.IGNORECASE),
]

WEAK_NON_RESUME_PATTERNS = [
    re.compile(r"\binvoice\b", re.IGNORECASE),
    re.compile(r"\breceipt\b", re.IGNORECASE),
    re.compile(r"\buser manual\b", re.IGNORECASE),
    re.compile(r"\bisbn\b", re.IGNORECASE),
    re.compile(r"\bprivacy policy\b", re.IGNORECASE),
    re.compile(r"\bterms and conditions\b", re.IGNORECASE),
]

RESUME_KEYWORD_PATTERN = re.compile(
    r"\b("
    r"experience|employment|work history|internship|education|qualification|"
    r"skills|technical skills|projects|certification|summary|objective|profile|"
    r"university|college|bachelor|master|b\.?\s*tech|m\.?\s*tech|developer|"
    r"engineer|analyst|manager|linkedin|github|portfolio|achievements|"
    r"responsibilities|curriculum vitae|resume|cv"
    r")\b",
    re.IGNORECASE,
)

YEAR_RANGE_PATTERN = re.compile(
    r"\b(19|20)\d{2}\s*[-–—to]+\s*((19|20)\d{2}|present|current)\b",
    re.IGNORECASE,
)

LINKEDIN_GITHUB_PATTERN = re.compile(r"\b(linkedin\.com|github\.com|gitlab\.com)\b", re.IGNORECASE)
BULLET_PATTERN = re.compile(r"^[\u2022\u2023\u25E6\u2043\u2219\-*●○◦▪▫]\s", re.MULTILINE)

MIN_TEXT_LENGTH = 80
MAX_PAGE_COUNT = 10
MIN_RESUME_SIGNALS = 2

RESUME_SECTION_KEYS = ("experience", "education", "skills", "projects", "summary", "certifications")


@dataclass
class ResumeValidationResult:
    is_valid: bool
    score: int = 0
    reasons: list[str] = field(default_factory=list)
    rejection_message: str = ""


class ResumeValidator:
    def validate(self, file_path: str) -> None:
        result = self.evaluate(file_path)
        if not result.is_valid:
            raise ValidationError(result.rejection_message)

    def evaluate(self, file_path: str) -> ResumeValidationResult:
        try:
            raw_text, extraction_meta = pdf_text_extractor.extract(file_path)
        except ValueError as exc:
            return ResumeValidationResult(is_valid=False, rejection_message=str(exc))

        text = sanitize_text(raw_text, max_length=50000)
        page_count = extraction_meta.get("page_count", 0)

        if page_count > MAX_PAGE_COUNT:
            return ResumeValidationResult(
                is_valid=False,
                rejection_message=(
                    f"This PDF has {page_count} pages. Please upload a resume or CV "
                    f"(typically {MAX_PAGE_COUNT} pages or fewer)."
                ),
            )

        if len(text) < MIN_TEXT_LENGTH:
            return ResumeValidationResult(
                is_valid=False,
                rejection_message=(
                    "This PDF does not contain enough readable text. "
                    "Image-only or scanned resumes without extractable text are not supported."
                ),
            )

        strong_non_resume = self._count_patterns(text, STRONG_NON_RESUME_PATTERNS)
        weak_non_resume = self._count_patterns(text, WEAK_NON_RESUME_PATTERNS)

        if strong_non_resume >= 2 or (strong_non_resume >= 1 and weak_non_resume >= 2):
            return ResumeValidationResult(
                is_valid=False,
                rejection_message=(
                    "This PDF appears to be a non-resume document (e.g. invoice, manual, or article). "
                    "Please upload a resume or CV only."
                ),
            )

        sections = section_parser.parse_sections(text)
        email = contact_extractor.extract_email(text)
        phone = contact_extractor.extract_phone(text)
        resume_keywords = len(RESUME_KEYWORD_PATTERN.findall(text[:12000]))
        has_month_dates = bool(DATE_RANGE_PATTERN.search(text))
        has_year_dates = bool(YEAR_RANGE_PATTERN.search(text))
        has_social_links = bool(LINKEDIN_GITHUB_PATTERN.search(text))
        has_email_in_text = bool(EMAIL_PATTERN.search(text))
        bullet_lines = len(BULLET_PATTERN.findall(text))
        section_count = sum(1 for key in RESUME_SECTION_KEYS if sections.get(key))

        signals = 0
        reasons: list[str] = []

        if email or has_email_in_text:
            signals += 1
            reasons.append("email found")
        if phone:
            signals += 1
            reasons.append("phone found")
        if section_count:
            signals += min(section_count, 3)
            reasons.append(f"{section_count} structured section(s)")
        if resume_keywords >= 2:
            signals += 2
            reasons.append(f"{resume_keywords} resume keywords")
        elif resume_keywords == 1:
            signals += 1
            reasons.append("resume keyword found")
        if has_month_dates or has_year_dates:
            signals += 1
            reasons.append("date range found")
        if has_social_links:
            signals += 1
            reasons.append("professional link found")
        if bullet_lines >= 3:
            signals += 1
            reasons.append("bullet-point content found")
        if len(text) >= 400 and resume_keywords >= 1:
            signals += 1
            reasons.append("substantial resume-like content")

        if signals >= MIN_RESUME_SIGNALS:
            return ResumeValidationResult(is_valid=True, score=signals, reasons=reasons)

        return ResumeValidationResult(
            is_valid=False,
            score=signals,
            reasons=reasons,
            rejection_message=(
                "This PDF does not appear to be a resume or CV. "
                "Please upload a document with your contact details, work history, education, or skills."
            ),
        )

    def _count_patterns(self, text: str, patterns: list[re.Pattern]) -> int:
        sample = text[:10000]
        return sum(1 for pattern in patterns if pattern.search(sample))


resume_validator = ResumeValidator()
