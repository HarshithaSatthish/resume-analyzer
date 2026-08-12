import json

from app.schemas.resume import ATSScoreBreakdown, ParsedResumeData
from app.services.gemini.constants import FEEDBACK_JSON_SCHEMA


class GeminiPromptBuilder:
    def build_feedback_prompt(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
        job_description: str | None = None,
    ) -> str:
        job_context = ""
        if job_description:
            job_context = f"""
Target Job Description:
{job_description[:4000]}

Tailor career suggestions and improvements to this role when relevant.
"""

        return f"""
Analyze the resume data below and return ONLY valid JSON.

Candidate Information:
- Name: {parsed_data.name or "Unknown"}
- Email: {parsed_data.email or "Not provided"}
- Phone: {parsed_data.phone or "Not provided"}
- Summary: {parsed_data.summary or "Not provided"}

Sections:
- Education: {json.dumps(parsed_data.education[:10], ensure_ascii=False)}
- Experience: {json.dumps(parsed_data.experience[:10], ensure_ascii=False)}
- Projects: {json.dumps(parsed_data.projects[:10], ensure_ascii=False)}
- Certifications: {json.dumps(parsed_data.certifications[:10], ensure_ascii=False)}
- Languages: {json.dumps(parsed_data.languages[:10], ensure_ascii=False)}

Skills Detected: {json.dumps(detected_skills[:30], ensure_ascii=False)}

ATS Scores:
- Overall: {ats_scores.overall_score}
- Formatting: {ats_scores.formatting_score}
- Skills: {ats_scores.skill_score}
- Experience: {ats_scores.experience_score}
- Keywords: {ats_scores.keyword_score}
- Grade: {ats_scores.grade or "N/A"}
- ATS Recommendations: {json.dumps(ats_scores.recommendations[:6], ensure_ascii=False)}
{job_context}
Return JSON with this exact structure:
{json.dumps(FEEDBACK_JSON_SCHEMA, indent=2)}

Requirements:
- resume_feedback: 2-4 sentences of holistic review
- career_suggestions: 3-5 specific career growth suggestions
- resume_improvements: 3-6 concrete resume edits
- professional_summary: a polished 2-3 sentence summary rewrite
- strengths: 3-5 bullet strengths
- weaknesses: 2-4 areas to improve
- recommended_certifications: 2-4 relevant certifications
- recommended_projects: 2-4 portfolio project ideas
"""


prompt_builder = GeminiPromptBuilder()
