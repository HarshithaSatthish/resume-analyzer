import json
import re

import spacy
from spacy.matcher import PhraseMatcher

from app.config import settings
from app.utils.text_utils import normalize_skill


class SkillExtractorService:
    def __init__(self) -> None:
        self._nlp = None
        self._matcher = None
        self._skills_catalog: list[str] = []

    def _load_skills_catalog(self) -> list[str]:
        dataset_path = settings.skills_dataset_path
        if not dataset_path.exists():
            return []

        with open(dataset_path, "r", encoding="utf-8") as dataset_file:
            data = json.load(dataset_file)

        skills: list[str] = []
        if isinstance(data, list):
            for item in data:
                if isinstance(item, str):
                    skills.append(normalize_skill(item))
                elif isinstance(item, dict) and item.get("name"):
                    skills.append(normalize_skill(str(item["name"])))
        elif isinstance(data, dict):
            for category_skills in data.values():
                if isinstance(category_skills, list):
                    for skill in category_skills:
                        if isinstance(skill, str):
                            skills.append(normalize_skill(skill))

        return sorted(set(skill for skill in skills if skill), key=len, reverse=True)

    def _ensure_matcher(self) -> None:
        if self._matcher is not None:
            return

        self._skills_catalog = self._load_skills_catalog()

        try:
            self._nlp = spacy.load(settings.spacy_model)
        except OSError:
            self._nlp = spacy.blank("en")

        self._matcher = PhraseMatcher(self._nlp.vocab, attr="LOWER")
        patterns = [self._nlp.make_doc(skill) for skill in self._skills_catalog]
        if patterns:
            self._matcher.add("SKILLS", patterns)

    def extract_skills(self, text: str, resume_skills: list[str] | None = None) -> list[str]:
        self._ensure_matcher()
        detected: set[str] = set()

        doc = self._nlp(text)
        matches = self._matcher(doc)
        for _, start, end in matches:
            span = doc[start:end].text.strip()
            detected.add(normalize_skill(span))

        if resume_skills:
            for skill in resume_skills:
                cleaned = normalize_skill(skill)
                if cleaned:
                    detected.add(cleaned)

        self._apply_regex_fallback(text, detected)
        return sorted(detected, key=str.lower)

    def _apply_regex_fallback(self, text: str, detected: set[str]) -> None:
        lowered_text = text.lower()
        for skill in self._skills_catalog:
            pattern = re.escape(skill.lower())
            if re.search(rf"\b{pattern}\b", lowered_text):
                detected.add(skill)


skill_extractor_service = SkillExtractorService()
