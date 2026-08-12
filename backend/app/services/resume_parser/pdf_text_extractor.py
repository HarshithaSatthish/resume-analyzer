import logging

import pdfplumber
from PyPDF2 import PdfReader

logger = logging.getLogger(__name__)


class PDFTextExtractor:
    def extract(self, file_path: str) -> tuple[str, dict]:
        text_parts: list[str] = []
        method = "pdfplumber"
        page_count = 0

        try:
            with pdfplumber.open(file_path) as pdf:
                page_count = len(pdf.pages)
                for page in pdf.pages:
                    page_text = page.extract_text(x_tolerance=2, y_tolerance=2) or ""
                    if page_text.strip():
                        text_parts.append(self._normalize_page_text(page_text))
        except Exception as exc:
            logger.warning("pdfplumber extraction failed: %s", exc)
            text_parts = []

        if not text_parts:
            method = "pypdf2"
            try:
                reader = PdfReader(file_path)
                page_count = len(reader.pages)
                for page in reader.pages:
                    page_text = page.extract_text() or ""
                    if page_text.strip():
                        text_parts.append(self._normalize_page_text(page_text))
            except Exception as exc:
                logger.error("PyPDF2 extraction failed: %s", exc)
                raise ValueError("Unable to extract text from the PDF. The file may be scanned or corrupted.") from exc

        if not text_parts:
            raise ValueError("No readable text found in the PDF. Image-only resumes are not supported.")

        combined = "\n".join(text_parts)
        metadata = {
            "page_count": page_count,
            "extraction_method": method,
            "character_count": len(combined),
            "line_count": len(combined.splitlines()),
        }
        return combined, metadata

    def _normalize_page_text(self, text: str) -> str:
        lines = [line.rstrip() for line in text.splitlines()]
        return "\n".join(line for line in lines if line.strip() or line == "")


pdf_text_extractor = PDFTextExtractor()
