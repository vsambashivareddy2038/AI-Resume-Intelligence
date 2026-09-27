import re


def clean_text(text):
    """
    Clean extracted resume text.
    """

    # Convert to lowercase
    text = text.lower()

    # Remove email addresses
    text = re.sub(
        r"\S+@\S+",
        " ",
        text
    )

    # Remove URLs
    text = re.sub(
        r"https?://\S+|www\.\S+",
        " ",
        text
    )

    # Replace new lines with spaces
    text = re.sub(
        r"\n+",
        " ",
        text
    )

    # Keep useful characters for technical skills
    text = re.sub(
        r"[^a-zA-Z0-9+#.\s]",
        " ",
        text
    )

    # Remove multiple spaces
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()