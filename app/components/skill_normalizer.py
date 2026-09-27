
import re

import pandas as pd


class SkillNormalizer:
    def __init__(self, skill_file="data/skills.csv"):
        self.skills = pd.read_csv(skill_file)
        self.skills["skill"] = (
            self.skills["skill"]
            .astype(str)
            .str.strip()
            .str.lower()
        )
        self.canonical_skills = sorted(
            self.skills["skill"]
            .dropna()
            .unique()
            .tolist()
        )
        self.aliases = self._build_aliases()

    def _clean(self, skill):
        # Convert the skill to a simple lowercase format.
        if not skill:
            return ""

        skill = str(skill).lower().strip()
        skill = skill.replace("–", "-")
        skill = skill.replace("—", "-")
        skill = re.sub(r"\s+", " ", skill)

        return skill.strip()

    def _build_aliases(self):
        # Map common skill names to their canonical names.
        aliases = {
            "py": "python",
            "python 2": "python",
            "python 3": "python",
            "python3": "python",
            "sklearn": "scikit-learn",
            "scikit learn": "scikit-learn",
            "scikit_learn": "scikit-learn",
            "powerbi": "power bi",
            "power-bi": "power bi",
            "power bi desktop": "power bi",
            "mysql": "mysql",
            "my sql": "mysql",
            "postgres": "postgresql",
            "postgre sql": "postgresql",
            "postgres sql": "postgresql",
            "js": "javascript",
            "java script": "javascript",
            "ts": "typescript",
            "type script": "typescript",
            "node": "node.js",
            "nodejs": "node.js",
            "node js": "node.js",
            "opencv-python": "opencv",
            "nlp": "nlp",
            "natural language processing": "natural language processing",
            "ml": "machine learning",
            "dl": "deep learning",
            "cv": "computer vision",
            "tf": "tensorflow",
            "torch": "pytorch",
            "git hub": "github",
            "power point": "powerpoint",
        }

        return aliases

    def normalize(self, skill):
        # Return the canonical skill name when a match is found.
        cleaned = self._clean(skill)

        if not cleaned:
            return None

        if cleaned in self.canonical_skills:
            return cleaned

        if cleaned in self.aliases:
            canonical = self.aliases[cleaned]
            if canonical in self.canonical_skills:
                return canonical

        # Remove version numbers such as Python 3 or Python 3.11.
        without_version = re.sub(
            r"\s+v?\d+(?:\.\d+)*$",
            "",
            cleaned
        ).strip()

        if without_version and without_version in self.canonical_skills:
            return without_version

        return None

    def normalize_list(self, skills):
        # Normalize all skills and remove duplicates.
        if not skills:
            return []

        normalized = []

        for skill in skills:
            canonical = self.normalize(skill)

            if canonical:
                normalized.append(canonical)

        return sorted(set(normalized))

    def normalize_project_technologies(self, projects):
        # Normalize the technologies used in each project.
        if not projects:
            return []

        normalized_projects = []

        for project in projects:
            project_copy = dict(project)
            technologies = project.get("technologies", [])

            project_copy["technologies"] = self.normalize_list(
                technologies
            )
            normalized_projects.append(project_copy)

        return normalized_projects

    def normalize_resume_information(self, resume_information):
        # Normalize resume skills and project technologies.
        if not resume_information:
            return {}

        normalized = dict(resume_information)

        normalized["skills"] = self.normalize_list(
            resume_information.get("skills", [])
        )

        normalized["projects"] = self.normalize_project_technologies(
            resume_information.get("projects", [])
        )

        return normalized

    def normalize_job_skills(self, required_skills, preferred_skills):
        # Normalize required and preferred job skills.
        return {
            "required": self.normalize_list(required_skills),
            "preferred": self.normalize_list(preferred_skills)
        }
