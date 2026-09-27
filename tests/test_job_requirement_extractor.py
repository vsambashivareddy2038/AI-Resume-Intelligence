from app.components.job_requirement_extractor import (
    JobRequirementExtractor
)


JOB_DESCRIPTION = """
Machine Learning Engineer

We are looking for a Machine Learning Engineer to design,
develop, and deploy machine learning solutions.

Responsibilities:

- Develop and implement machine learning models.
- Build and maintain machine learning pipelines.
- Perform data preprocessing and feature engineering.
- Analyze datasets and identify useful patterns.

Required Skills:

- Python
- Machine Learning
- Deep Learning
- Pandas
- NumPy
- Scikit-learn
- TensorFlow
- PyTorch
- Natural Language Processing
- SQL
- Git
- Docker
- FastAPI

Preferred Skills:

- Computer Vision
- OpenCV
- YOLO
- Streamlit
- AWS

Education:

- Bachelor's degree in Computer Science,
  Artificial Intelligence, Data Science,
  or a related field.

Experience:

- 0–2 years of experience in machine learning,
  data science, or software development.
"""


def test_extract_role():

    extractor = JobRequirementExtractor()

    result = extractor.extract(
        JOB_DESCRIPTION
    )

    assert (
        result["role"]
        == "Machine Learning Engineer"
    )


def test_extract_required_skills():

    extractor = JobRequirementExtractor()

    result = extractor.extract(
        JOB_DESCRIPTION
    )

    required = result[
        "skills"
    ][
        "required"
    ]

    assert "python" in required

    assert "machine learning" in required

    assert "deep learning" in required

    assert "pandas" in required

    assert "numpy" in required

    assert "scikit-learn" in required

    assert "tensorflow" in required

    assert "pytorch" in required

    assert "sql" in required

    assert "git" in required

    assert "docker" in required

    assert "fastapi" in required


def test_preferred_skills():

    extractor = JobRequirementExtractor()

    result = extractor.extract(
        JOB_DESCRIPTION
    )

    preferred = result[
        "skills"
    ][
        "preferred"
    ]

    assert "computer vision" in preferred

    assert "opencv" in preferred

    assert "yolo" in preferred

    assert "streamlit" in preferred

    assert "aws" in preferred


def test_education():

    extractor = JobRequirementExtractor()

    result = extractor.extract(
        JOB_DESCRIPTION
    )

    education = result[
        "education"
    ]

    assert (
        education["degree_level"]
        == "bachelor"
    )

    assert (
        "computer science"
        in education["fields"]
    )

    assert (
        "artificial intelligence"
        in education["fields"]
    )

    assert (
        "data science"
        in education["fields"]
    )


def test_experience():

    extractor = JobRequirementExtractor()

    result = extractor.extract(
        JOB_DESCRIPTION
    )

    experience = result[
        "experience"
    ]

    assert (
        experience[
            "experience_required"
        ]
        is True
    )

    assert (
        experience[
            "min_years"
        ]
        == 0.0
    )

    assert (
        experience[
            "max_years"
        ]
        == 2.0
    )


def test_empty_jd():

    extractor = JobRequirementExtractor()

    result = extractor.extract("")

    assert (
        result["role"]
        is None
    )

    assert (
        result["skills"]["required"]
        == []
    )

    assert (
        result["skills"]["preferred"]
        == []
    )

    assert (
        result["education"]["degree_level"]
        is None
    )

    assert (
        result["experience"][
            "experience_required"
        ]
        is False
    )