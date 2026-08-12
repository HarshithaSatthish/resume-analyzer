from pathlib import Path

from app.middleware.error_handler import ValidationError
from app.schemas.resume import ParsedResumeData, ParseMetadata, ParseResponse
from app.services.resume_parser.contact_extractor import contact_extractor
from app.services.resume_parser.pdf_text_extractor import pdf_text_extractor
from app.services.resume_parser.section_parser import section_parser
from app.utils.text_utils import sanitize_text


class ResumeParserService:
    def parse_pdf(self, file_path: str) -> ParsedResumeData:
        return self.parse_pdf_with_metadata(file_path).parsed_data

    def parse_pdf_with_metadata(self, file_path: str) -> ParseResponse:
        path = Path(file_path)
        if not path.exists():
            raise ValidationError("Resume file not found.")

        raw_text, extraction_meta = pdf_text_extractor.extract(str(path))
        cleaned_text = sanitize_text(raw_text, max_length=50000)

        email = contact_extractor.extract_email(cleaned_text)
        phone = contact_extractor.extract_phone(cleaned_text)
        name = contact_extractor.extract_name(cleaned_text, email)

        sections = section_parser.parse_sections(cleaned_text)

        parsed = ParsedResumeData(
            name=name,
            email=email,
            phone=phone,
            education=sections["education"],
            projects=sections["projects"],
            experience=sections["experience"],
            skills=sections["skills"],
            certifications=sections["certifications"],
            languages=sections["languages"],
            summary=sections.get("summary", [""])[0] if sections.get("summary") else "",
            raw_text=cleaned_text,
        )

        metadata = ParseMetadata(
            page_count=extraction_meta["page_count"],
            extraction_method=extraction_meta["extraction_method"],
            character_count=extraction_meta["character_count"],
            line_count=extraction_meta["line_count"],
            sections_found=self._count_sections(parsed),
            contact_fields_found=self._count_contact_fields(parsed),
        )

        return ParseResponse(parsed_data=parsed, metadata=metadata)

    def _count_sections(self, parsed: ParsedResumeData) -> int:
        sections = [
            parsed.education,
            parsed.experience,
            parsed.projects,
            parsed.skills,
            parsed.certifications,
            parsed.languages,
        ]
        return sum(1 for section in sections if section)

    def _count_contact_fields(self, parsed: ParsedResumeData) -> int:
        fields = [parsed.name, parsed.email, parsed.phone]
        return sum(1 for field in fields if field)


resume_parser_service = ResumeParserService()
