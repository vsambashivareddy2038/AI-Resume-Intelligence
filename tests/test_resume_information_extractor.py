from app.components.resume_information_extractor import ResumeInformationExtractor


def test_unified_resume_information_extractor():
    resume_text = """
    John Doe
    john.doe@gmail.com
    +91 9876543210
    github.com/johndoe

    SUMMARY

    AI and Machine Learning enthusiast.

    EDUCATION

    B.Tech in Computer Science and Engineering
    ABC Institute of Technology
    2028

    EXPERIENCE

    Machine Learning Intern
    ABC Technologies
    June 2025 - August 2025
    Developed machine learning models.

    Software Developer Intern
    XYZ Solutions
    January 2026 - May 2026
    Developed backend applications.

    PROJECTS

    AI Resume Intelligence System

    Developed an AI-powered resume analysis system.

    Technologies: Python, Streamlit, FastAPI, Machine Learning, NLP

    Smart Traffic Monitoring System

    Developed a real-time traffic monitoring system.

    Technologies: Python, YOLO, OpenCV

    SKILLS

    Python
    Machine Learning
    FastAPI
    Streamlit
    OpenCV
    SQL

    CERTIFICATIONS

    Python Certification
    Coursera
    2025

    Machine Learning Certification
    Udemy
    2026

    ACHIEVEMENTS

    ZENTRON 2026 Hackathon - Merit Certificate
    2026

    Coding Competition Winner
    2025
    """

    extractor = ResumeInformationExtractor()
    result = extractor.extract(resume_text)

    # Check that the main sections are returned.
    expected_keys = {
        "personal_information",
        "education",
        "experience",
        "projects",
        "skills",
        "skill_categories",
        "sections"
    }
    assert expected_keys.issubset(result.keys())

    # Check the extracted email.
    assert result["personal_information"]["email"] == "john.doe@gmail.com"

    # Check that education details were extracted.
    assert result["education"]["degree"] is not None

    # Check the total experience.
    assert len(result["experience"]["entries"]) == 2
    assert result["experience"]["total_experience_months"] == 6
    assert result["experience"]["total_experience_years"] == 0.5

    # Check the first experience entry.
    first_experience = result["experience"]["entries"][0]
    assert first_experience["title"] == "Machine Learning Intern"
    assert first_experience["company"] == "ABC Technologies"
    assert first_experience["start_date"] == "June 2025"
    assert first_experience["end_date"] == "August 2025"
    assert first_experience["duration_months"] == 2

    # Check the second experience entry.
    second_experience = result["experience"]["entries"][1]
    assert second_experience["title"] == "Software Developer Intern"
    assert second_experience["company"] == "XYZ Solutions"
    assert second_experience["start_date"] == "January 2026"
    assert second_experience["end_date"] == "May 2026"
    assert second_experience["duration_months"] == 4

    # Check that both projects were extracted.
    assert len(result["projects"]) == 2
    project_names = [project["name"] for project in result["projects"]]
    assert "AI Resume Intelligence System" in project_names
    assert "Smart Traffic Monitoring System" in project_names

    # Check the extracted skills.
    assert "python" in result["skills"]
    assert "machine learning" in result["skills"]
    assert "fastapi" in result["skills"]
    assert "streamlit" in result["skills"]
    assert "opencv" in result["skills"]
    assert "sql" in result["skills"]

    # Check the skill categories.
    assert "programming" in result["skill_categories"]
    assert "machine_learning" in result["skill_categories"]
    assert "web" in result["skill_categories"]

    # Check that the expected resume sections were detected.
    assert result["sections"]["education"] is True
    assert result["sections"]["experience"] is True
    assert result["sections"]["projects"] is True
    assert result["sections"]["skills"] is True
    assert result["sections"]["certifications"] is True
    assert result["sections"]["achievements"] is True
    assert result["sections"]["summary"] is True
