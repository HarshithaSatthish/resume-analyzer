from app.schemas.report import JobComparisonResult
from app.services.skill_extractor_service import skill_extractor_service
from app.utils.text_utils import extract_keywords, normalize_skill


class ComparisonService:
    def compare_with_job_description(
        self,
        resume_text: str,
        detected_skills: list[str],
        job_description: str,
    ) -> JobComparisonResult:
        job_skills = skill_extractor_service.extract_skills(job_description)
        job_keywords = sorted(extract_keywords(job_description))

        resume_skill_set = {normalize_skill(skill).lower() for skill in detected_skills}
        job_skill_set = {normalize_skill(skill).lower() for skill in job_skills}

        matched_skills = sorted(
            skill for skill in detected_skills if normalize_skill(skill).lower() in job_skill_set
        )
        missing_skills = sorted(
            skill for skill in job_skills if normalize_skill(skill).lower() not in resume_skill_set
        )

        if job_skill_set:
            match_percentage = round((len(matched_skills) / len(job_skill_set)) * 100, 2)
        else:
            resume_keywords = extract_keywords(resume_text)
            job_keyword_set = set(job_keywords)
            overlap = resume_keywords.intersection(job_keyword_set)
            match_percentage = round((len(overlap) / max(len(job_keyword_set), 1)) * 100, 2)

        return JobComparisonResult(
            match_percentage=min(match_percentage, 100.0),
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            job_keywords=job_keywords[:50],
        )


comparison_service = ComparisonService()
