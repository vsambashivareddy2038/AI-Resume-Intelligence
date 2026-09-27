from app.components.experience_extractor import (
    ExperienceExtractor
)


def test_experience_extraction():

    text = """
    Samba Shiva Reddy

    EXPERIENCE

    Machine Learning Intern
    ABC Technologies
    June 2025 - August 2025

    Developed machine learning models.

    Software Developer Intern
    XYZ Solutions
    January 2026 - May 2026

    Developed backend applications.

    EDUCATION

    B.Tech
    """

    extractor = ExperienceExtractor()

    result = extractor.extract(text)


    assert len(
        result["entries"]
    ) == 2


    first = result["entries"][0]


    assert (
        first["title"]
        == "Machine Learning Intern"
    )


    assert (
        first["company"]
        == "ABC Technologies"
    )


    assert (
        first["start_date"]
        == "June 2025"
    )


    assert (
        first["end_date"]
        == "August 2025"
    )


    assert (
        first["type"]
        == "Internship"
    )


    assert (
        first["duration_months"]
        == 2
    )


    assert (
        result["total_experience_months"]
        == 6
    )

