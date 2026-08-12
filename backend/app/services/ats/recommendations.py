from app.schemas.resume import ATSScoreBreakdown, ParsedResumeData


class ATSRecommendationEngine:
    THRESHOLD = 70.0

    def generate(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        scores: ATSScoreBreakdown,
    ) -> list[str]:
        recommendations: list[str] = []

        if not parsed_data.name or not parsed_data.email:
            recommendations.append("Add complete contact information including your full name and professional email.")

        if scores.formatting_score < self.THRESHOLD:
            recommendations.append("Improve resume formatting with clear section headings and consistent bullet points.")

        if scores.skill_score < self.THRESHOLD:
            recommendations.append("Expand your skills section with role-relevant technologies and tools.")

        if scores.experience_score < self.THRESHOLD:
            recommendations.append("Strengthen experience entries with measurable achievements and date ranges.")

        if scores.education_score < self.THRESHOLD:
            recommendations.append("Include education details such as degree, institution, and graduation timeline.")

        if scores.project_score < self.THRESHOLD:
            recommendations.append("Add project entries that demonstrate practical application of your skills.")

        if scores.keyword_score < self.THRESHOLD:
            recommendations.append("Incorporate stronger action verbs and quantifiable results throughout the resume.")

        if scores.readability_score < self.THRESHOLD:
            recommendations.append("Use concise bullet points and shorter sentences to improve readability.")

        if len(detected_skills) < 8:
            recommendations.append("Increase technical keyword coverage to improve ATS matching for target roles.")

        if not parsed_data.summary:
            recommendations.append("Add a professional summary at the top to highlight your core value proposition.")

        if scores.overall_score >= 85 and not recommendations:
            recommendations.append("Your resume is ATS-ready. Tailor keywords for each job application.")

        return recommendations[:8]


recommendation_engine = ATSRecommendationEngine()
