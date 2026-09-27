import re
import pandas as pd

class ProjectExtractor:

    PROJECT_HEADINGS = {
        "projects",
        "project",
        "academic projects",
        "personal projects",
        "project experience",
    }

    STOP_HEADINGS = {
        "education",
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "skills",
        "technical skills",
        "certifications",
        "certificates",
        "achievements",
        "awards",
        "summary",
        "profile",
        "career objective",
        "objective",
        "languages",
        "hobbies",
        "interests",
        "references",
    }

    TECHNOLOGY_PATTERNS = [
        "technologies:",
        "technology:",
        "tech stack:",
        "techstack:",
        "tools:",
        "frameworks:",
        "libraries:",
    ]

    DESCRIPTION_STARTERS = [
        "developed",
        "created",
        "built",
        "designed",
        "implemented",
        "analyzed",
        "cleaned",
        "managed",
        "worked",
        "responsible",
        "using",
        "used",
        "this project",
        "the system",
        "the application",
        "the project",
        "a real-time",
        "an ai-powered",
    ]

    def __init__(self, skill_file="data/skills.csv"):
        self.skill_file = skill_file

        try:
            self.skills = pd.read_csv(skill_file)

            self.skills["skill"] = (
                self.skills["skill"]
                .astype(str)
                .str.lower()
                .str.strip()
            )

            self.skill_list = (
                self.skills["skill"]
                .dropna()
                .unique()
                .tolist()
            )

        except Exception:
            self.skills = pd.DataFrame(
                columns=["skill", "category"]
            )
            self.skill_list = []

    # BASIC HELPERS

    def _clean_line(self, line):
        line = line.strip()

        line = re.sub(
            r"^[•●▪◦*-]\s*",
            "",
            line
        )

        return line.strip()

    def _is_project_heading(self, line):
        return (
            self._clean_line(line).lower()
            in self.PROJECT_HEADINGS
        )

    def _is_stop_heading(self, line):
        return (
            self._clean_line(line).lower()
            in self.STOP_HEADINGS
        )

    def _is_year_only(self, line):
        return bool(
            re.fullmatch(
                r"(?:19|20)\d{2}",
                line.strip()
            )
        )

    def _is_technology_line(self, line):
        lower = line.lower().strip()

        return any(
            lower.startswith(pattern)
            for pattern in self.TECHNOLOGY_PATTERNS
        )

    # DESCRIPTION DETECTION

    def _is_description_line(self, line):
        text = self._clean_line(line)

        if not text:
            return True

        lower = text.lower()

        if self._is_technology_line(text):
            return True

        if self._is_year_only(text):
            return True

        # Explicit description starters
        for starter in self.DESCRIPTION_STARTERS:
            if lower.startswith(starter):
                return True

        # A line ending in punctuation is usually prose.
        if text.endswith((".", "!", "?")):
            return True

        # These are common sentence patterns.
        sentence_patterns = [
            r"\bfor\s+\w+",
            r"\bwith\s+\w+",
            r"\busing\s+\w+",
            r"\band\s+\w+",
            r"\bthat\s+\w+",
            r"\bwhich\s+\w+",
            r"\bfrom\s+\w+",
            r"\bto\s+\w+",
        ]

        for pattern in sentence_patterns:
            if re.search(pattern, lower):
                return True

        # IMPORTANT:
        # Long lines are much more likely to be descriptions
        # than project names.
        if len(text.split()) > 6:
            return True

        return False

    # PROJECT TITLE DETECTION

    def _looks_like_project_title(
        self,
        line,
        previous_line=None,
        next_line=None
    ):
        text = self._clean_line(line)

        if not text:
            return False

        # Comma-separated lines are normally technology lists
        # or description text, not project titles.
        if "," in text:
            return False

        if self._is_project_heading(text):
            return False

        if self._is_stop_heading(text):
            return False

        if self._is_technology_line(text):
            return False

        if self._is_year_only(text):
            return False

        # Most important check:
        # description lines must never become project titles.
        if self._is_description_line(text):
            return False

        # GitHub / GitLab / Demo format

        if re.search(
            r"\|\s*(github|gitlab|demo|source code)\s*$",
            text,
            re.IGNORECASE
        ):
            return True

        words = text.split()

        if len(words) > 6:
            return False

        # Project titles in resumes normally use title case.
        # Examples:
        # AI Resume Intelligence System
        # Smart Traffic Monitoring System
        # Myntra Product Analysis Dashboard

        capitalized_count = sum(
            1
            for word in words
            if word[:1].isupper()
        )

        if (
            len(words) >= 2
            and capitalized_count == len(words)
        ):
            return True

        # One-word project names can be valid.
        if len(words) == 1:
            if words[0][:1].isupper():
                return True

        # If the following line is clearly a description,
        # a title-like current line is valid.
        if next_line:

            next_clean = self._clean_line(
                next_line
            )

            if self._is_description_line(
                next_clean
            ):

                if (
                    len(words) <= 6
                    and capitalized_count >= len(words) - 1
                ):
                    return True

        return False

    # PROJECT NAME

    def _clean_project_name(self, title):

        title = re.sub(
            r"\s*\|\s*(github|gitlab|demo|source code)\s*$",
            "",
            title,
            flags=re.IGNORECASE
        )

        return title.strip()

    # SKILL EXTRACTION

    def _extract_skills(self, text):

        if not text:
            return []

        text_lower = text.lower()

        found_skills = []

        for skill in self.skill_list:

            pattern = (
                r"(?<!\w)"
                + re.escape(skill)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                text_lower
            ):
                found_skills.append(skill)

        return sorted(
            set(found_skills)
        )

    # CATEGORY EXTRACTION

    def _get_categories(self, skills):

        categories = {}

        for skill in skills:

            rows = self.skills[
                self.skills["skill"] == skill
            ]

            if rows.empty:
                continue

            category = rows.iloc[0]["category"]

            categories.setdefault(
                category,
                []
            ).append(skill)

        return categories

    # TECHNOLOGY EXTRACTION

    def _extract_technology_text(
        self,
        lines
    ):

        technology_lines = []

        for line in lines:

            if self._is_technology_line(line):
                technology_lines.append(line)

        return " ".join(
            technology_lines
        ).lower().strip()

    # DESCRIPTION EXTRACTION

    def _extract_description(
        self,
        lines
    ):

        description_lines = []

        for line in lines:

            if self._is_technology_line(line):
                continue

            if self._is_year_only(line):
                continue

            description_lines.append(line)

        return " ".join(
            description_lines
        ).strip()

    # MAIN EXTRACTION

    def extract(self, text):

        if not text or not text.strip():
            return {
                "projects": [],
                "project_count": 0,
            }

        raw_lines = text.splitlines()

        lines = []

        for line in raw_lines:

            cleaned = self._clean_line(line)

            if cleaned:
                lines.append(cleaned)

        # Find PROJECTS heading

        start_index = None

        for index, line in enumerate(lines):

            if self._is_project_heading(line):
                start_index = index + 1
                break

        if start_index is None:
            return {
                "projects": [],
                "project_count": 0,
            }

        # Find end of PROJECTS section

        end_index = len(lines)

        for i in range(
            start_index,
            len(lines)
        ):

            if self._is_stop_heading(lines[i]):
                end_index = i
                break

        project_lines = lines[
            start_index:end_index
        ]

        # Detect project titles

        title_indexes = []

        for i, line in enumerate(
            project_lines
        ):

            previous_line = None
            next_line = None

            if i > 0:
                previous_line = project_lines[i - 1]

            if i + 1 < len(project_lines):
                next_line = project_lines[i + 1]

            if self._looks_like_project_title(
                line,
                previous_line,
                next_line
            ):
                title_indexes.append(i)

        # Remove duplicates while preserving order.
        title_indexes = list(
            dict.fromkeys(title_indexes)
        )

        # Build projects

        projects = []

        for position, title_index in enumerate(
            title_indexes
        ):

            title = self._clean_project_name(
                project_lines[title_index]
            )

            if position + 1 < len(title_indexes):
                next_title_index = (
                    title_indexes[position + 1]
                )
            else:
                next_title_index = len(
                    project_lines
                )

            block_start = title_index + 1
            block_end = next_title_index

            block_lines = project_lines[
                block_start:block_end
            ]

            block_text = " ".join(
                block_lines
            )

            technology_text = (
                self._extract_technology_text(
                    block_lines
                )
            )

            description = (
                self._extract_description(
                    block_lines
                )
            )

            skills = self._extract_skills(
                block_text
            )

            categories = self._get_categories(
                skills
            )

            projects.append({
                "name": title,
                "title": title,
                "description": description,
                "technologies": technology_text,
                "skills": skills,
                "skill_categories": categories,
            })

        return {
            "projects": projects,
            "project_count": len(projects),
        }
