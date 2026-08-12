class SkillScorer:
    def score(self, detected_skills: list[str], parsed_skills: list[str] | None = None) -> float:
        count = len(detected_skills)
        if count == 0:
            return 15.0

        base = self._count_score(count)
        diversity_bonus = self._diversity_bonus(detected_skills)
        alignment_bonus = self._alignment_bonus(detected_skills, parsed_skills or [])

        return min(round(base + diversity_bonus + alignment_bonus, 2), 100.0)

    def _count_score(self, count: int) -> float:
        if count < 3:
            return 35.0
        if count < 6:
            return 55.0
        if count < 10:
            return 72.0
        if count < 15:
            return 85.0
        if count < 25:
            return 93.0
        return 100.0

    def _diversity_bonus(self, skills: list[str]) -> float:
        categories = set()
        for skill in skills:
            lowered = skill.lower()
            if any(tag in lowered for tag in ("python", "java", "javascript", "react", "node")):
                categories.add("language")
            if any(tag in lowered for tag in ("aws", "docker", "kubernetes", "cloud")):
                categories.add("cloud")
            if any(tag in lowered for tag in ("sql", "mongo", "database")):
                categories.add("database")
            if any(tag in lowered for tag in ("leadership", "communication", "agile")):
                categories.add("soft")

        return min(len(categories) * 2, 8.0)

    def _alignment_bonus(self, detected: list[str], parsed: list[str]) -> float:
        if not parsed:
            return 0.0
        detected_set = {skill.lower() for skill in detected}
        parsed_set = {skill.lower() for skill in parsed}
        if not parsed_set:
            return 0.0
        overlap = len(detected_set.intersection(parsed_set))
        ratio = overlap / len(parsed_set)
        return min(ratio * 7, 7.0)


skill_scorer = SkillScorer()
