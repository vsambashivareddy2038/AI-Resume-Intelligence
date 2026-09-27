import os
import re
import tempfile

from app.components.resume_parser import extract_resume_text
from app.components.skill_extractor import SkillExtractor
from app.components.matcher import SemanticMatcher
from app.components.ats_scorer import ATSScorer
from app.components.resume_sections import detect_sections
from app.components.resume_quality import ResumeQualityAnalyzer
from app.components.resume_information_extractor import ResumeInformationExtractor
from app.components.job_requirement_extractor import JobRequirementExtractor
from app.components.skill_normalizer import SkillNormalizer
from app.ml_predictor import CandidateJobMatcher


skill_extractor = SkillExtractor()
semantic_matcher = SemanticMatcher()
ats_scorer = ATSScorer()
resume_quality_analyzer = ResumeQualityAnalyzer()
resume_information_extractor = ResumeInformationExtractor()
job_requirement_extractor = JobRequirementExtractor()
skill_normalizer = SkillNormalizer()
ml_matcher = CandidateJobMatcher()


def _unique_skills(skills):
    result = []
    seen = set()

    for skill in skills or []:
        if skill is None:
            continue

        skill = str(skill).strip().lower()

        if skill and skill not in seen:
            seen.add(skill)
            result.append(skill)

    return result


def _normalize_jd_text(text):
    if not text:
        return ""

    text = str(text)
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = text.replace("\u2013", "-")
    text = text.replace("\u2014", "-")
    text = text.replace("\u2022", "-")
    text = text.replace("\u25cf", "-")
    text = text.replace("\u25aa", "-")

    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def _prepare_jd_sections(text):
    text = _normalize_jd_text(text)

    headings = [
        "required skills",
        "required technical skills",
        "technical skills required",
        "mandatory skills",
        "must have skills",
        "preferred skills",
        "preferred technical skills",
        "desired skills",
        "nice to have",
        "good to have",
        "education",
        "educational requirements",
        "qualifications",
        "experience",
        "experience requirements",
        "responsibilities",
        "about the role",
        "job title",
        "requirements"
    ]

    pattern = "|".join(
        re.escape(item)
        for item in sorted(headings, key=len, reverse=True)
    )

    text = re.sub(
        rf"(?i)\s+(?=(?:{pattern})\s*:)",
        "\n",
        text
    )

    text = re.sub(
        rf"(?i)(?<!^)(?<!\n)(?=(?:{pattern})\s*:)",
        "\n",
        text
    )

    return text.strip()


def _extract_section(text, headings, stop_headings):
    text = _prepare_jd_sections(text)

    if not text:
        return ""

    heading_pattern = "|".join(
        re.escape(item)
        for item in sorted(headings, key=len, reverse=True)
    )

    stop_pattern = "|".join(
        re.escape(item)
        for item in sorted(stop_headings, key=len, reverse=True)
    )

    pattern = (
        rf"(?is)(?:^|\n)\s*(?:[-*]\s*)?"
        rf"(?:{heading_pattern})\s*:\s*(.*?)"
        rf"(?=\n\s*(?:[-*]\s*)?(?:{stop_pattern})\s*:|\Z)"
    )

    match = re.search(pattern, text)

    if match:
        return match.group(1).strip()

    return ""


def _extract_skills_from_jd_sections(job_description):
    required_headings = [
        "required skills",
        "required technical skills",
        "technical skills required",
        "mandatory skills",
        "must have skills"
    ]

    preferred_headings = [
        "preferred skills",
        "preferred technical skills",
        "desired skills",
        "nice to have",
        "good to have"
    ]

    all_headings = required_headings + preferred_headings + [
        "education",
        "educational requirements",
        "qualifications",
        "experience",
        "experience requirements",
        "responsibilities",
        "about the role",
        "job title",
        "requirements"
    ]

    required_text = _extract_section(
        job_description,
        required_headings,
        [
            item
            for item in all_headings
            if item not in required_headings
        ]
    )

    preferred_text = _extract_section(
        job_description,
        preferred_headings,
        [
            item
            for item in all_headings
            if item not in preferred_headings
        ]
    )

    required_skills = (
        skill_extractor.extract_skills(required_text)
        if required_text
        else []
    )

    preferred_skills = (
        skill_extractor.extract_skills(preferred_text)
        if preferred_text
        else []
    )

    required_skills = _unique_skills(required_skills)
    preferred_skills = _unique_skills(preferred_skills)

    preferred_set = set(preferred_skills)

    required_skills = [
        skill
        for skill in required_skills
        if skill not in preferred_set
    ]

    return required_skills, preferred_skills


def _extract_job_requirements(job_description):
    structured = job_requirement_extractor.extract(
        job_description
    )

    if not isinstance(structured, dict):
        structured = {}

    education = structured.get("education", {})
    experience = structured.get("experience", {})

    if not isinstance(education, dict):
        education = {}

    if not isinstance(experience, dict):
        experience = {}

    required_skills, preferred_skills = (
        _extract_skills_from_jd_sections(
            job_description
        )
    )

    structured_skills = structured.get("skills", {})

    if not isinstance(structured_skills, dict):
        structured_skills = {}

    if not required_skills:
        required_skills = _unique_skills(
            structured_skills.get("required", [])
        )

    if not preferred_skills:
        preferred_skills = _unique_skills(
            structured_skills.get("preferred", [])
        )

    if not required_skills:
        all_skills = structured.get("skills", [])

        if isinstance(all_skills, list):
            required_skills = _unique_skills(
                all_skills
            )

    return {
        "role": structured.get("role"),
        "required_skills": _unique_skills(
            required_skills
        ),
        "preferred_skills": _unique_skills(
            preferred_skills
        ),
        "education": education,
        "experience": experience
    }


def save_uploaded_file(file_content, filename):
    suffix = os.path.splitext(filename)[1]

    temp_file = tempfile.NamedTemporaryFile(
        delete=False,
        suffix=suffix
    )

    try:
        temp_file.write(file_content)
        temp_file.flush()
    finally:
        temp_file.close()

    return temp_file.name


def analyze_resume_file(file_content, filename):
    file_path = save_uploaded_file(
        file_content,
        filename
    )

    try:
        resume_text = extract_resume_text(
            file_path
        )

        skills = _unique_skills(
            skill_extractor.extract_skills(
                resume_text
            )
        )

        categories = skill_extractor.get_categories(
            skills
        )

        sections = detect_sections(
            resume_text
        )

        quality = resume_quality_analyzer.analyze(
            resume_text,
            sections
        )

        structured_information = (
            resume_information_extractor.extract(
                resume_text
            )
        )

        structured_information = (
            skill_normalizer.normalize_resume_information(
                structured_information
            )
        )

        return {
            "filename": filename,
            "text": resume_text,
            "personal_information": structured_information.get(
                "personal_information",
                {}
            ),
            "education": structured_information.get(
                "education",
                {}
            ),
            "experience": structured_information.get(
                "experience",
                {
                    "entries": [],
                    "total_experience_months": 0,
                    "total_experience_years": 0.0
                }
            ),
            "projects": structured_information.get(
                "projects",
                []
            ),
            "project_count": structured_information.get(
                "project_count",
                0
            ),
            "skills": skills,
            "skill_categories": categories,
            "categories": categories,
            "sections": sections,
            "quality": quality
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)


def match_resume_with_job(
    file_content,
    filename,
    job_description
):
    file_path = save_uploaded_file(
        file_content,
        filename
    )

    try:
        resume_text = extract_resume_text(
            file_path
        )

        resume_information = (
            resume_information_extractor.extract(
                resume_text
            )
        )

        resume_information = (
            skill_normalizer.normalize_resume_information(
                resume_information
            )
        )

        resume_skills = _unique_skills(
            resume_information.get(
                "skills",
                []
            )
        )

        job_data = _extract_job_requirements(
            job_description
        )

        required_skills = job_data[
            "required_skills"
        ]

        matched_skills = ats_scorer.matched_skills(
            resume_skills,
            required_skills
        )

        missing_skills = ats_scorer.missing_skills(
            resume_skills,
            required_skills
        )

        skill_score = ats_scorer.calculate_skill_match(
            resume_skills,
            required_skills
        )

        semantic_score = (
            semantic_matcher.calculate_similarity(
                resume_text,
                job_description
            )
        )

        experience = resume_information.get(
            "experience",
            {}
        )

        education = resume_information.get(
            "education",
            {}
        )

        sections = resume_information.get(
            "sections",
            {}
        )

        experience_score = (
            ats_scorer.calculate_experience_score(
                experience
            )
        )

        education_score = (
            ats_scorer.calculate_education_score(
                education
            )
        )

        structure_score = (
            ats_scorer.calculate_structure_score(
                sections
            )
        )

        experience_requirement_score = (
            ats_scorer.calculate_requirement_experience_score(
                experience,
                job_data["experience"]
            )
        )

        education_requirement_score = (
            ats_scorer.calculate_requirement_education_score(
                education,
                job_data["education"]
            )
        )

        ats_score = ats_scorer.requirement_aware_score(
            skill_score=skill_score,
            preferred_skill_score=0.0,
            semantic_score=semantic_score,
            experience_requirement_score=(
                experience_requirement_score
            ),
            education_requirement_score=(
                education_requirement_score
            ),
            structure_score=structure_score
        )

        experience_years = (
            ml_matcher._extract_experience_years(
                experience
            )
        )

        expected_experience_years = (
            ml_matcher._get_expected_experience(
                job_data["experience"]
            )
        )

        ml_candidate = {
            "roles": ml_matcher._extract_roles(
                experience
            ),
            "skills_primary": resume_skills,
            "skills_secondary": [],
            "experience_years": experience_years,
            "domains": [],
            "career_intent": ""
        }

        ml_job = {
            "title": job_data.get("role") or "",
            "description": job_description,
            "experience_years_hint": (
                expected_experience_years
            ),
            "remote_hint": ml_matcher._get_remote_hint(
                job_description
            )
        }

        ml_result = ml_matcher.predict(
            ml_candidate,
            ml_job
        )

        return {
            "ats_score": ats_score,
            "skill_score": skill_score,
            "semantic_score": semantic_score,
            "experience_score": experience_score,
            "education_score": education_score,
            "structure_score": structure_score,
            "matched_skills": _unique_skills(
                matched_skills
            ),
            "missing_skills": _unique_skills(
                missing_skills
            ),
            "required_skills": required_skills,
            "ml_match_probability": (
                ml_result["match_probability"]
            ),
            "ml_match_category": (
                ml_result["match_category"]
            ),
            "ml_model_prediction": (
                ml_result["model_prediction"]
            ),
            "ml_matched_skills": (
                ml_result["matched_skills"]
            ),
            "ml_features": ml_result["features"]
        }

    finally:
        if os.path.exists(file_path):
            os.remove(file_path)