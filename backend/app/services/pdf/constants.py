from reportlab.lib import colors

BRAND_PRIMARY = colors.HexColor("#4F46E5")
BRAND_DARK = colors.HexColor("#312E81")
TABLE_HEADER_BG = colors.HexColor("#EEF2FF")
TABLE_GRID = colors.HexColor("#C7D2FE")
TABLE_ROW_ALT = colors.HexColor("#F8FAFC")

CHART_COLORS = ["#6366F1", "#8B5CF6", "#3B82F6", "#06B6D4", "#10B981", "#F59E0B", "#EC4899"]

SCORE_METRICS = [
    ("formatting_score", "Formatting", "15%"),
    ("keyword_score", "Keywords", "10%"),
    ("skill_score", "Skills", "25%"),
    ("project_score", "Projects", "15%"),
    ("education_score", "Education", "10%"),
    ("experience_score", "Experience", "20%"),
    ("readability_score", "Readability", "5%"),
]

PARSED_SECTIONS = [
    ("summary", "Professional Summary"),
    ("education", "Education"),
    ("experience", "Experience"),
    ("projects", "Projects"),
    ("certifications", "Certifications"),
]
