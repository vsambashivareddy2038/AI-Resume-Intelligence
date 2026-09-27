from app.components.education_extractor import (
    EducationExtractor
)


def test_education_extraction():

    text = """
    Samba Shiva Reddy

    EDUCATION

    B.Tech in Computer Science and Engineering (AI & ML)
    DRK Institute of Science and Technology
    JNTUH
    2024 - 2028

    Intermediate
    Sri Chaitanya Junior College
    2022 - 2024

    SSC
    ABC High School
    2022
    """

    extractor = EducationExtractor()

    result = extractor.extract(text)


    assert result["degree"] == "B.Tech"


    assert "B.Tech" in result["degrees"]

    assert "Intermediate" in result["degrees"]

    assert "SSC" in result["degrees"]


    assert (
        result["institution"]
        == "DRK Institute of Science and Technology"
    )


    assert (
        result["specialization"]
        == "computer science and engineering"
    )


    assert (
        result["graduation_year"]
        == "2028"
    )

