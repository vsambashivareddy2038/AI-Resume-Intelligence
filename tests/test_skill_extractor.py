from app.components.resume_parser import (
    extract_resume_text
)

from app.components.skill_extractor import (
    SkillExtractor
)


def test_skill_extraction():

    text = extract_resume_text(
        "data/sample_resumes/resume.pdf"
    )

    extractor = SkillExtractor()

    skills = extractor.extract_skills(
        text
    )

    print(
        "\n========== SKILLS ==========\n"
    )

    for skill in skills:

        print(
            "✓",
            skill
        )

    assert isinstance(
        skills,
        list
    )