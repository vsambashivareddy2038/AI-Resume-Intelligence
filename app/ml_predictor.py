from pathlib import Path
import re
import joblib
import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"
TRAINING_DIR = PROJECT_ROOT / "data" / "training"


FEATURES = [
    "candidate_experience_years",
    "candidate_skill_count",
    "expected_experience_years",
    "experience_gap",
    "experience_fit",
    "job_skill_count",
    "matched_skill_count",
    "job_skill_coverage",
    "candidate_skill_coverage",
    "role_match_score",
    "job_remote_hint",
    "semantic_similarity"
]


class CandidateJobMatcher:

    def __init__(self):
        self.model = joblib.load(
            MODELS_DIR / "random_forest_match_model.pkl"
        )

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.cleaned_data = pd.read_pickle(
            TRAINING_DIR / "candidate_job_cleaned.pkl"
        )

        self.skill_vocabulary = self._build_skill_vocabulary()

    def _build_skill_vocabulary(self):
        vocabulary = set()

        for column in [
            "candidate_skills_primary",
            "candidate_skills_secondary"
        ]:
            if column not in self.cleaned_data.columns:
                continue

            for skills in self.cleaned_data[column]:
                if isinstance(skills, list):
                    for skill in skills:
                        vocabulary.add(str(skill).lower())

        return vocabulary

    def _extract_experience_years(self, experience):
        if not experience:
            return 0.0

        if isinstance(experience, (int, float)):
            return float(experience)

        if isinstance(experience, dict):
            for key in [
                "total_experience_years",
                "experience_years",
                "years",
                "total_years"
            ]:
                value = experience.get(key)
                if isinstance(value, (int, float)):
                    return float(value)

        text = str(experience).lower()

        years = re.findall(
            r"(\d+(?:\.\d+)?)\s*(?:years?|yrs?)",
            text
        )

        if years:
            return max(float(value) for value in years)

        months = re.findall(
            r"(\d+)\s*(?:months?|mos?)",
            text
        )

        if months:
            return max(float(value) / 12 for value in months)

        return 0.0

    def _get_expected_experience(self, experience_requirements):
        if isinstance(experience_requirements, (int, float)):
            return float(experience_requirements)

        if isinstance(experience_requirements, dict):
            for key in [
                "min_years",
                "minimum_years",
                "years",
                "experience_years",
                "required_years",
                "min_experience"
            ]:
                value = experience_requirements.get(key)
                if isinstance(value, (int, float)):
                    return float(value)

        text = str(experience_requirements).lower()

        matches = re.findall(
            r"(\d+(?:\.\d+)?)\s*\+?\s*years?",
            text
        )

        if matches:
            return max(float(value) for value in matches)

        return 0.0

    def _extract_roles(self, experience):
        roles = []

        if isinstance(experience, dict):
            entries = experience.get("entries", [])
        elif isinstance(experience, list):
            entries = experience
        else:
            entries = []

        for entry in entries:
            if not isinstance(entry, dict):
                continue

            for key in [
                "role",
                "title",
                "position",
                "designation",
                "job_title"
            ]:
                value = entry.get(key)
                if isinstance(value, str) and value.strip():
                    roles.append(value.strip())
                    break

        return list(dict.fromkeys(roles))

    def _get_remote_hint(self, job_text):
        text = job_text.lower()

        remote_words = [
            "remote",
            "work from home",
            "work-from-home",
            "wfh"
        ]

        return int(any(word in text for word in remote_words))

    def _calculate_features(self, candidate, job):
        primary_skills = candidate.get(
            "skills_primary",
            []
        )

        secondary_skills = candidate.get(
            "skills_secondary",
            []
        )

        candidate_skills = list(
            dict.fromkeys(
                str(skill)
                for skill in primary_skills + secondary_skills
                if str(skill).strip()
            )
        )

        candidate_skill_count = len(candidate_skills)

        candidate_skills_lower = [
            skill.lower()
            for skill in candidate_skills
        ]

        job_title = str(job.get("title", ""))
        job_description = str(job.get("description", ""))
        job_text = (
            job_title + " " + job_description
        ).lower()

        job_skills = [
            skill
            for skill in self.skill_vocabulary
            if skill in job_text
        ]

        job_skills = list(dict.fromkeys(job_skills))

        matched_skills = [
            skill
            for skill in job_skills
            if skill in candidate_skills_lower
        ]

        matched_skills = list(dict.fromkeys(matched_skills))

        job_skill_count = len(job_skills)
        matched_skill_count = len(matched_skills)

        if job_skill_count > 0:
            job_skill_coverage = (
                matched_skill_count / job_skill_count
            )
        else:
            job_skill_coverage = 0.0

        if candidate_skill_count > 0:
            candidate_skill_coverage = (
                matched_skill_count / candidate_skill_count
            )
        else:
            candidate_skill_coverage = 0.0

        candidate_experience_years = float(
            candidate.get("experience_years", 0) or 0
        )

        expected_experience_years = float(
            job.get("experience_years_hint", 0) or 0
        )

        experience_gap = (
            candidate_experience_years
            - expected_experience_years
        )

        experience_fit = (
            1
            - abs(experience_gap)
            / (expected_experience_years + 1)
        )

        experience_fit = float(
            np.clip(experience_fit, 0, 1)
        )

        candidate_roles = candidate.get("roles", [])

        candidate_role_text = " ".join(
            str(role)
            for role in candidate_roles
        ).lower()

        job_title_words = set(
            job_title.lower().split()
        )

        candidate_role_words = set(
            candidate_role_text.split()
        )

        if job_title_words:
            role_match_score = (
                len(
                    job_title_words
                    & candidate_role_words
                )
                / len(job_title_words)
            )
        else:
            role_match_score = 0.0

        candidate_text = " ".join(
            [
                str(value)
                for value in (
                    candidate_roles
                    + primary_skills
                    + secondary_skills
                    + candidate.get("domains", [])
                    + [candidate.get("career_intent", "")]
                )
            ]
        )

        job_full_text = (
            job_title + " " + job_description
        )

        candidate_embedding = self.embedding_model.encode(
            [candidate_text],
            convert_to_numpy=True
        )[0]

        job_embedding = self.embedding_model.encode(
            [job_full_text],
            convert_to_numpy=True
        )[0]

        candidate_norm = np.linalg.norm(candidate_embedding)
        job_norm = np.linalg.norm(job_embedding)

        if candidate_norm == 0 or job_norm == 0:
            semantic_similarity = 0.0
        else:
            semantic_similarity = (
                np.dot(
                    candidate_embedding,
                    job_embedding
                )
                / (candidate_norm * job_norm)
            )

        features = pd.DataFrame([{
            "candidate_experience_years": candidate_experience_years,
            "candidate_skill_count": candidate_skill_count,
            "expected_experience_years": expected_experience_years,
            "experience_gap": experience_gap,
            "experience_fit": experience_fit,
            "job_skill_count": job_skill_count,
            "matched_skill_count": matched_skill_count,
            "job_skill_coverage": job_skill_coverage,
            "candidate_skill_coverage": candidate_skill_coverage,
            "role_match_score": role_match_score,
            "job_remote_hint": job.get("remote_hint", 0),
            "semantic_similarity": semantic_similarity
        }])

        return features, matched_skills

    def predict(self, candidate, job):
        features, matched_skills = self._calculate_features(
            candidate,
            job
        )

        features = features[FEATURES]

        probability = float(
            self.model.predict_proba(features)[0][1]
        )

        prediction = int(
            self.model.predict(features)[0]
        )

        percentage = probability * 100

        if probability >= 0.75:
            category = "Excellent Match"
        elif probability >= 0.50:
            category = "Good Match"
        elif probability >= 0.25:
            category = "Moderate Match"
        else:
            category = "Poor Match"

        return {
            "match_probability": round(percentage, 2),
            "match_category": category,
            "model_prediction": prediction,
            "matched_skills": matched_skills,
            "features": features.to_dict(orient="records")[0]
        }
