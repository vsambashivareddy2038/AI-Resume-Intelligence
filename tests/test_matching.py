from app.components.matcher import (
    SemanticMatcher
)


def test_semantic_matching():

    resume = """

    Computer Science student with experience
    in Python, machine learning, data analysis,
    Pandas, NumPy and SQL.

    """

    job = """

    We are seeking a Machine Learning Engineer
    with strong Python programming skills,
    machine learning and data science experience.

    """

    matcher = SemanticMatcher()

    score = matcher.calculate_similarity(
        resume,
        job
    )

    print(
        "\nSemantic Similarity:",
        score,
        "%"
    )

    assert score >= 0

    assert score <= 100