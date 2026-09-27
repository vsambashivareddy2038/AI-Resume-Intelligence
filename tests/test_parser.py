from app.components.resume_parser import (
    extract_resume_text
)

from app.utils.text_cleaner import (
    clean_text
)


def test_pdf_parser():

    file_path = (
        "data/sample_resumes/resume.pdf"
    )

    text = extract_resume_text(
        file_path
    )

    assert text is not None

    assert len(text) > 0


if __name__ == "__main__":

    file_path = (
        "data/sample_resumes/resume.pdf"
    )

    text = extract_resume_text(
        file_path
    )

    print("\n========== RESUME TEXT ==========\n")

    print(text)

    print("\n=================================\n")

    print(
        "Characters:",
        len(text)
    )

    print(
        "Words:",
        len(text.split())
    )




raw_text = extract_resume_text(
    "data/sample_resumes/resume.pdf"
)

cleaned_text = clean_text(
    raw_text
)

print("\n========== CLEANED TEXT ==========\n")

print(cleaned_text)