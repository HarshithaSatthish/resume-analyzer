from app.schemas.resume import AIFeedback, ATSScoreBreakdown, ParsedResumeData


class GeminiFallbackGenerator:
    def generate(
        self,
        parsed_data: ParsedResumeData,
        detected_skills: list[str],
        ats_scores: ATSScoreBreakdown,
    ) -> AIFeedback:
        strengths: list[str] = []
        weaknesses: list[str] = []
        improvements: list[str] = []

        if detected_skills:
            strengths.append(f"Strong skill coverage with {len(detected_skills)} detected skills.")
            top_skills = ", ".join(detected_skills[:5])
            strengths.append(f"Key skills include {top_skills}.")
        else:
            weaknesses.append("Limited technical skills detected in the resume.")
            improvements.append("Add a dedicated skills section with role-relevant technologies.")

        if parsed_data.experience:
            strengths.append("Professional experience section is present with structured entries.")
        else:
            weaknesses.append("Experience section is missing or unclear.")
            improvements.append("Include measurable achievements in your work experience.")

        if parsed_data.projects:
            strengths.append("Projects section adds practical credibility.")
        else:
            improvements.append("Add 2-3 projects that demonstrate applied skills.")

        if parsed_data.education:
            strengths.append("Education background is documented.")
        else:
            weaknesses.append("Education section could be more prominent.")

        if ats_scores.overall_score < 70:
            improvements.append("Improve ATS compatibility with clearer section headings and keywords.")

        if ats_scores.recommendations:
            improvements.extend(ats_scores.recommendations[:3])

        summary_name = parsed_data.name or "The candidate"
        skill_text = ", ".join(detected_skills[:5]) or "multiple domains"

        return AIFeedback(
            resume_feedback=(
                f"{summary_name}'s resume achieved an ATS score of {ats_scores.overall_score} "
                f"(Grade {ats_scores.grade or 'N/A'}). "
                "Focus on strengthening weak sections and aligning content with target roles."
            ),
            career_suggestions=[
                "Tailor your resume for each job application.",
                "Highlight quantifiable results in experience bullets.",
                "Build portfolio projects aligned with your target role.",
                "Network with professionals in your desired industry.",
            ],
            resume_improvements=improvements or [
                "Use consistent formatting and bullet points.",
                "Add role-specific keywords from job descriptions.",
            ],
            professional_summary=(
                parsed_data.summary
                or f"{summary_name} is a motivated professional with expertise in {skill_text}."
            ),
            strengths=strengths or ["Resume contains foundational professional information."],
            weaknesses=weaknesses or ["Some sections could be expanded with stronger impact statements."],
            recommended_certifications=[
                "Google Professional Certificate in your domain",
                "AWS Certified Cloud Practitioner",
                "Industry-specific certification aligned with your target role",
            ],
            recommended_projects=[
                "End-to-end full-stack application with deployment",
                "Data analysis or automation project with documented outcomes",
                "Open-source contribution demonstrating collaboration skills",
            ],
            source="fallback",
            model="rule-based-fallback",
        )


fallback_generator = GeminiFallbackGenerator()
