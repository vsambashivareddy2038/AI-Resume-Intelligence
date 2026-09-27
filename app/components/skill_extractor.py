import pandas as pd
import re


class SkillExtractor:

    def __init__(
        self,
        skill_file="data/skills.csv"
    ):

        self.skills = pd.read_csv(
            skill_file
        )

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


    def extract_skills(self, text):

        text = text.lower()

        found_skills = []

        for skill in self.skill_list:

            pattern = (
                r"(?<!\w)"
                + re.escape(skill)
                + r"(?!\w)"
            )

            if re.search(
                pattern,
                text
            ):

                found_skills.append(
                    skill
                )

        return sorted(
            set(found_skills)
        )


    def get_categories(
        self,
        skills
    ):

        result = {}

        for skill in skills:

            rows = self.skills[
                self.skills["skill"] == skill
            ]

            if not rows.empty:

                category = rows.iloc[0][
                    "category"
                ]

                result.setdefault(
                    category,
                    []
                ).append(skill)

        return result