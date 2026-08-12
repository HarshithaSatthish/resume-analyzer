from app.schemas.resume import ATSScoreBreakdown, ParsedResumeData
from app.services.ats.constants import ATS_WEIGHTS, GRADE_THRESHOLDS
from app.services.ats.formatting_scorer import formatting_scorer
from app.services.ats.keyword_scorer import keyword_scorer
from app.services.ats.readability_scorer import readability_scorer
from app.services.ats.recommendations import recommendation_engine
from app.services.ats.section_scorer import section_scorer
from app.services.ats.skill_scorer import skill_scorer


class ATSResult:
    def __init__(self, scores: ATSScoreBreakdown, weights: dict[str, float]):
        self.scores = scores
        self.weights = weights


class ATSService:
    def calculate_scores(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
    ) -> ATSScoreBreakdown:
        return self.calculate_full_result(parsed_data, detected_skills).scores

    def calculate_full_result(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
    ) -> ATSResult:
        formatting_score = formatting_scorer.score(parsed_data)
        skill_score = skill_scorer.score(detected_skills, parsed_data.skills)
        project_score = section_scorer.score_projects(parsed_data.projects)
        education_score = section_scorer.score_education(parsed_data.education)
        experience_score = section_scorer.score_experience(parsed_data.experience)
        keyword_score = keyword_scorer.score(parsed_data.raw_text)
        readability_score = readability_scorer.score(parsed_data.raw_text)

        overall_score = round(
            formatting_score * ATS_WEIGHTS["formatting"]
            + skill_score * ATS_WEIGHTS["skills"]
            + project_score * ATS_WEIGHTS["projects"]
            + education_score * ATS_WEIGHTS["education"]
            + experience_score * ATS_WEIGHTS["experience"]
            + keyword_score * ATS_WEIGHTS["keywords"]
            + readability_score * ATS_WEIGHTS["readability"],
            2,
        )
        overall_score = min(overall_score, 100.0)
        grade = self._calculate_grade(overall_score)

        base_scores = ATSScoreBreakdown(
            overall_score=overall_score,
            formatting_score=formatting_score,
            keyword_score=keyword_score,
            skill_score=skill_score,
            project_score=project_score,
            education_score=education_score,
            experience_score=experience_score,
            readability_score=readability_score,
            grade=grade,
            recommendations=[],
        )

        recommendations = recommendation_engine.generate(parsed_data, detected_skills, base_scores)
        scores = base_scores.model_copy(update={"recommendations": recommendations})

        return ATSResult(scores=scores, weights=ATS_WEIGHTS.copy())

    def _calculate_grade(self, score: float) -> str:
        for threshold, grade in GRADE_THRESHOLDS:
            if score >= threshold:
                return grade
        return "F"


ats_service = ATSService()
