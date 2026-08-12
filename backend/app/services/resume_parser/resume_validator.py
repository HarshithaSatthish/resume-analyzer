import re
from dataclasses import dataclass, field

from app.middleware.error_handler import ValidationError
from app.services.resume_parser.constants import DATE_RANGE_PATTERN
from app.services.resume_parser.contact_extractor import contact_extractor
from app.services.resume_parser.pdf_text_extractor import pdf_text_extractor
from app.services.resume_parser.section_parser import section_parser
from app.utils.text_utils import sanitize_text

NON_RESUME_PATTERNS = [
    re.compile(r"\binvoice\b", re.IGNORECASE),
    re.compile(r"\btax invoice\b", re.IGNORECASE),
    re.compile(r"\bbill to\b", re.IGNORECASE),
    re.compile(r"\bship to\b", re.IGNORECASE),
    re.compile(r"\bamount due\b", re.IGNORECASE),
    re.compile(r"\bpayment due\b", re.IGNORECASE),
    re.compile(r"\breceipt\b", re.IGNORECASE),
    re.compile(r"\border confirmation\b", re.IGNORECASE),
    re.compile(r"\btracking number\b", re.IGNORECASE),
    re.compile(r"\bbank statement\b", re.IGNORECASE),
    re.compile(r"\baccount statement\b", re.IGNORECASE),
    re.compile(r"\btransaction history\b", re.IGNORECASE),
    re.compile(r"\btable of contents\b", re.IGNORECASE),
    re.compile(r"\bchapter\s+\d+\b", re.IGNORECASE),
    re.compile(r"\bisbn\b", re.IGNORECASE),
    re.compile(r"\buser manual\b", re.IGNORECASE),
    re.compile(r"\binstruction manual\b", re.IGNORECASE),
    re.compile(r"\bwarranty\b", re.IGNORECASE),
    re.compile(r"\bprivacy policy\b", re.IGNORECASE),
    re.compile(r"\bterms of service\b", re.IGNORECASE),
    re.compile(r"\bterms and conditions\b", re.IGNORECASE),
    re.compile(r"\bmedical report\b", re.IGNORECASE),
    re.compile(r"\bprescription\b", re.IGNORECASE),
    re.compile(r"\bnutrition facts\b", re.IGNORECASE),
    re.compile(r"\bingredients\s*:", re.IGNORECASE),
    re.compile(r"\bproduct catalog\b", re.IGNORECASE),
    re.compile(r"\bbrochure\b", re.IGNORECASE),
    re.compile(r"\bsyllabus\b", re.IGNORECASE),
    re.compile(r"\bcourse outline\b", re.IGNORECASE),
]

RESUME_TITLE_PATTERN = re.compile(
    r"\b(curriculum vitae|resume|résumé|cv)\b",
    re.IGNORECASE,
)

MIN_TEXT_LENGTH = 180
MAX_PAGE_COUNT = 8
MIN_RESUME_SCORE = 4
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
                    "This PDF does not contain enough readable text to be a resume. "
                    "Image-only or scanned documents without text are not supported."
                ),
            )

        non_resume_hits = self._count_non_resume_signals(text)
        if non_resume_hits >= 2:
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
        has_date_ranges = bool(DATE_RANGE_PATTERN.search(text))
        has_resume_title = bool(RESUME_TITLE_PATTERN.search(text[:1500]))

        score = 0
        reasons: list[str] = []

        section_count = sum(1 for key in RESUME_SECTION_KEYS if sections.get(key))
        if section_count:
            score += section_count * 2
            reasons.append(f"{section_count} resume section(s) detected")

        if email:
            score += 2
            reasons.append("contact email found")
        if phone:
            score += 1
            reasons.append("phone number found")
        if has_date_ranges:
            score += 2
            reasons.append("employment or education dates found")
        if has_resume_title:
            score += 1
            reasons.append("resume/CV title found")

        has_core_section = any(sections.get(key) for key in ("experience", "education", "skills", "projects"))
        has_contact = bool(email or phone)

        if non_resume_hits == 1:
            score -= 2

        if not has_core_section and not (has_contact and has_date_ranges):
            return ResumeValidationResult(
                is_valid=False,
                score=score,
                reasons=reasons,
                rejection_message=(
                    "This PDF does not look like a resume. Expected sections such as "
                    "Experience, Education, or Skills, along with contact details."
                ),
            )

        if score < MIN_RESUME_SCORE:
            return ResumeValidationResult(
                is_valid=False,
                score=score,
                reasons=reasons,
                rejection_message=(
                    "This PDF does not appear to be a resume or CV. "
                    "Please upload a document with work history, education, or skills."
                ),
            )

        return ResumeValidationResult(is_valid=True, score=score, reasons=reasons)

    def _count_non_resume_signals(self, text: str) -> int:
        sample = text[:8000]
        return sum(1 for pattern in NON_RESUME_PATTERNS if pattern.search(sample))


resume_validator = ResumeValidator()
