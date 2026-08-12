import re

SECTION_HEADERS: dict[str, list[str]] = {
    "summary": [
        "summary",
        "professional summary",
        "profile",
        "about me",
        "objective",
        "career objective",
    ],
    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "employment",
        "work history",
        "career history",
        "internship",
        "internships",
    ],
    "education": [
        "education",
        "academic background",
        "academic qualifications",
        "qualifications",
        "educational background",
    ],
    "projects": [
        "projects",
        "personal projects",
        "academic projects",
        "key projects",
        "portfolio",
        "project experience",
    ],
    "skills": [
        "skills",
        "technical skills",
        "core competencies",
        "competencies",
        "technologies",
        "tools",
        "tech stack",
        "skills & tools",
    ],
    "certifications": [
        "certifications",
        "certificates",
        "licenses",
        "credentials",
        "professional certifications",
    ],
    "languages": [
        "languages",
        "language proficiency",
        "language skills",
    ],
}

SECTION_SKIP_LINES = {
    "resume",
    "curriculum vitae",
    "cv",
    "page",
}

EMAIL_PATTERN = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")

PHONE_PATTERNS = [
    re.compile(r"\+?\d{1,3}[\s.-]?\(?\d{2,4}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b"),
    re.compile(r"\b\d{3}[\s.-]\d{3}[\s.-]\d{4}\b"),
    re.compile(r"\b\(\d{3}\)\s*\d{3}[\s.-]?\d{4}\b"),
]

DATE_RANGE_PATTERN = re.compile(
    r"\b(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}\s*[-–—to]+\s*(?:present|current|(?:jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*\.?\s+\d{4}|\d{4})\b",
    re.IGNORECASE,
)

BULLET_PREFIX_PATTERN = re.compile(r"^[\u2022\u2023\u25E6\u2043\u2219\-*●○◦▪▫]\s*")

SKILL_DELIMITERS = re.compile(r"[,|;/•\n]|(?:\s{2,})")

MAX_SECTION_ITEMS = 25
MAX_SKILL_ITEMS = 50
