import re

from app.components.education_extractor import EducationExtractor
from app.components.experience_extractor import ExperienceExtractor
from app.components.project_extractor import ProjectExtractor
from app.components.skill_extractor import SkillExtractor
from app.components.resume_sections import detect_sections


class ResumeInformationExtractor:

    def __init__(self, skill_file="data/skills.csv"):
        self.education_extractor = EducationExtractor()
        self.experience_extractor = ExperienceExtractor()
        self.project_extractor = ProjectExtractor()
        self.skill_extractor = SkillExtractor(skill_file)

    def _extract_personal_information(self, resume_text):
        email_match = re.search(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            resume_text
        )

        phone_match = re.search(
            r"(?:\+91[\s-]?)?[6-9]\d{9}",
            resume_text
        )

        github_match = re.search(
            r"(?:https?://)?(?:www\.)?github\.com/[A-Za-z0-9_.-]+",
            resume_text,
            re.IGNORECASE
        )

        lines = [
            line.strip()
            for line in resume_text.splitlines()
            if line.strip()
        ]

        name = ""

        if lines:
            first_line = lines[0]

            if (
                "@" not in first_line
                and not re.search(r"\d", first_line)
                and len(first_line.split()) <= 5
            ):
                name = first_line

        return {
            "name": name,
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0) if phone_match else None,
            "github": github_match.group(0) if github_match else None
        }

    def extract(self, resume_text):

        if not resume_text or not resume_text.strip():
            return {
                "personal_information": {},
                "education": {},
                "experience": {
                    "entries": [],
                    "total_experience_months": 0,
                    "total_experience_years": 0.0
                },
                "projects": [],
                "project_count": 0,
                "skills": [],
                "skill_categories": {},
                "sections": {}
            }

        personal_information = self._extract_personal_information(
            resume_text
        )

        education = self.education_extractor.extract(
            resume_text
        )

        experience = self.experience_extractor.extract(
            resume_text
        )

        project_data = self.project_extractor.extract(
            resume_text
        )

        projects = project_data.get(
            "projects",
            []
        )

        project_count = project_data.get(
            "project_count",
            len(projects)
        )

        skills = self.skill_extractor.extract_skills(
            resume_text
        )

        skill_categories = self.skill_extractor.get_categories(
            skills
        )

        sections = detect_sections(
            resume_text
        )

        return {
            "personal_information": personal_information,
            "education": education,
            "experience": experience,
            "projects": projects,
            "project_count": project_count,
            "skills": skills,
            "skill_categories": skill_categories,
            "sections": sections
        }