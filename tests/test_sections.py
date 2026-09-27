from app.components.resume_parser import (
    extract_resume_text
)

from app.components.resume_sections import (
    detect_sections
)


def test_sections():

    text = extract_resume_text(
        "data/sample_resumes/resume.pdf"
    )

    sections = detect_sections(text)

    print("\n========== SECTIONS ==========\n")

    for section, found in sections.items():

        status = "FOUND" if found else "MISSING"

        print(
            f"{section}: {status}"
        )

    assert isinstance(
        sections,
        dict
    )