from app.components.ats_scorer import ATSScorer


def test_skill_match():
    scorer = ATSScorer()

    resume_skills = [
        "python",
        "pandas",
        "numpy"
    ]

    required_skills = [
        "python",
        "pandas",
        "sql"
    ]

    score = scorer.calculate_skill_match(
        resume_skills,
        required_skills
    )

    assert score == 66.67


def test_matched_skills():
    scorer = ATSScorer()

    resume_skills = [
        "python",
        "pandas",
        "numpy"
    ]

    required_skills = [
        "python",
        "pandas",
        "sql"
    ]

    matched = scorer.matched_skills(
        resume_skills,
        required_skills
    )

    assert matched == [
        "python",
        "pandas"
    ]


def test_missing_skills():
    scorer = ATSScorer()

    resume_skills = [
        "python",
        "pandas",
        "numpy"
    ]

    required_skills = [
        "python",
        "pandas",
        "sql"
    ]

    missing = scorer.missing_skills(
        resume_skills,
        required_skills
    )

    assert missing == [
        "sql"
    ]


def test_experience_score_no_experience():
    scorer = ATSScorer()

    experience_data = {
        "entries": [],
        "total_experience_months": 0,
        "total_experience_years": 0.0
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 0.0


def test_experience_score_internship():
    scorer = ATSScorer()

    experience_data = {
        "entries": [
            {
                "title": "Machine Learning Intern",
                "company": "ABC Technologies",
                "start_date": "June 2025",
                "end_date": "August 2025",
                "duration_months": 2,
                "type": "Internship"
            }
        ],
        "total_experience_months": 2,
        "total_experience_years": 0.17
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 50.0


def test_experience_score_six_months():
    scorer = ATSScorer()

    experience_data = {
        "entries": [
            {
                "title": "Machine Learning Intern",
                "company": "ABC Technologies",
                "start_date": "June 2025",
                "end_date": "December 2025",
                "duration_months": 6,
                "type": "Internship"
            }
        ],
        "total_experience_months": 6,
        "total_experience_years": 0.5
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 60.0


def test_experience_score_one_year():
    scorer = ATSScorer()

    experience_data = {
        "entries": [
            {
                "title": "Software Developer",
                "company": "ABC Technologies",
                "start_date": "January 2025",
                "end_date": "January 2026",
                "duration_months": 12,
                "type": "Full-time"
            }
        ],
        "total_experience_months": 12,
        "total_experience_years": 1.0
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 70.0


def test_experience_score_two_years():
    scorer = ATSScorer()

    experience_data = {
        "entries": [
            {
                "title": "Software Developer",
                "company": "ABC Technologies",
                "start_date": "January 2024",
                "end_date": "January 2026",
                "duration_months": 24,
                "type": "Full-time"
            }
        ],
        "total_experience_months": 24,
        "total_experience_years": 2.0
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 80.0


def test_experience_score_three_years():
    scorer = ATSScorer()

    experience_data = {
        "entries": [
            {
                "title": "Software Developer",
                "company": "ABC Technologies",
                "start_date": "January 2023",
                "end_date": "January 2026",
                "duration_months": 36,
                "type": "Full-time"
            }
        ],
        "total_experience_months": 36,
        "total_experience_years": 3.0
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 90.0


def test_experience_score_five_years():
    scorer = ATSScorer()

    experience_data = {
        "entries": [
            {
                "title": "Senior Software Developer",
                "company": "ABC Technologies",
                "start_date": "January 2021",
                "end_date": "January 2026",
                "duration_months": 60,
                "type": "Full-time"
            }
        ],
        "total_experience_months": 60,
        "total_experience_years": 5.0
    }

    score = scorer.calculate_experience_score(
        experience_data
    )

    assert score == 100.0


def test_education_score_empty():
    scorer = ATSScorer()

    education_data = {}

    score = scorer.calculate_education_score(
        education_data
    )

    assert score == 0.0


def test_education_score_degree_only():
    scorer = ATSScorer()

    education_data = {
        "degree": "B.Tech",
        "degrees": ["B.Tech"],
        "institution": None,
        "specialization": None,
        "graduation_year": None
    }

    score = scorer.calculate_education_score(
        education_data
    )

    assert score == 50.0


def test_education_score_degree_and_institution():
    scorer = ATSScorer()

    education_data = {
        "degree": "B.Tech",
        "degrees": ["B.Tech"],
        "institution": "DRK Institute of Science and Technology",
        "specialization": None,
        "graduation_year": None
    }

    score = scorer.calculate_education_score(
        education_data
    )

    assert score == 70.0


def test_education_score_degree_institution_specialization():
    scorer = ATSScorer()

    education_data = {
        "degree": "B.Tech",
        "degrees": ["B.Tech"],
        "institution": "DRK Institute of Science and Technology",
        "specialization": "CSE AI ML",
        "graduation_year": None
    }

    score = scorer.calculate_education_score(
        education_data
    )

    assert score == 85.0


def test_education_score_complete():
    scorer = ATSScorer()

    education_data = {
        "degree": "B.Tech",
        "degrees": ["B.Tech"],
        "institution": "DRK Institute of Science and Technology",
        "specialization": "CSE AI ML",
        "graduation_year": 2028
    }

    score = scorer.calculate_education_score(
        education_data
    )

    assert score == 100.0


def test_structure_score_empty():
    scorer = ATSScorer()

    sections = {}

    score = scorer.calculate_structure_score(
        sections
    )

    assert score == 0.0


def test_structure_score_basic_student_resume():
    scorer = ATSScorer()

    sections = {
        "education": True,
        "experience": False,
        "skills": True,
        "projects": True,
        "certifications": False,
        "achievements": False,
        "summary": False
    }

    score = scorer.calculate_structure_score(
        sections
    )

    assert score == 60.0


def test_structure_score_with_experience():
    scorer = ATSScorer()

    sections = {
        "education": True,
        "experience": True,
        "skills": True,
        "projects": True,
        "certifications": False,
        "achievements": False,
        "summary": False
    }

    score = scorer.calculate_structure_score(
        sections
    )

    assert score == 75.0


def test_structure_score_complete_resume():
    scorer = ATSScorer()

    sections = {
        "education": True,
        "experience": True,
        "skills": True,
        "projects": True,
        "certifications": True,
        "achievements": True,
        "summary": True
    }

    score = scorer.calculate_structure_score(
        sections
    )

    assert score == 100.0


def test_overall_score():
    scorer = ATSScorer()

    score = scorer.overall_score(
        skill_score=80,
        semantic_score=70,
        experience_score=60,
        education_score=90,
        structure_score=80
    )

    expected = (
        80 * 0.40
        + 70 * 0.30
        + 60 * 0.15
        + 90 * 0.10
        + 80 * 0.05
    )

    assert score == round(expected, 2)