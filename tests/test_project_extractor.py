from app.components.project_extractor import (
    ProjectExtractor
)


def test_project_extraction():

    text = """
    Samba Shiva Reddy

    PROJECTS

    AI Resume Intelligence System

    Developed an AI-powered resume analysis
    system for ATS scoring and career
    recommendations.

    Technologies: Python, Streamlit, FastAPI,
    Machine Learning, NLP

    Smart Traffic Monitoring System

    Developed a real-time traffic monitoring
    application using computer vision.

    Technologies: Python, YOLO, OpenCV

    EDUCATION

    B.Tech Computer Science
    """


    extractor = ProjectExtractor()

    result = extractor.extract(
        text
    )


    assert (
        result["project_count"]
        == 2
    )


    first_project = (
        result["projects"][0]
    )


    assert (
        first_project["name"]
        == "AI Resume Intelligence System"
    )


    assert (
        "python"
        in first_project["technologies"]
    )


    assert (
        "streamlit"
        in first_project["technologies"]
    )


    assert (
        "fastapi"
        in first_project["technologies"]
    )


    second_project = (
        result["projects"][1]
    )


    assert (
        second_project["name"]
        == "Smart Traffic Monitoring System"
    )


    assert (
        "python"
        in second_project["technologies"]
    )


    assert (
        "yolo"
        in second_project["technologies"]
    )

