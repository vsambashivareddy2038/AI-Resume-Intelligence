import re


SECTION_PATTERNS = {

    "education": [
        "education",
        "academic background",
        "qualifications",
        "academic qualifications"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment"
    ],

    "skills": [
        "skills",
        "technical skills",
        "technical knowledge",
        "technologies"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "project experience"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "certification"
    ],

    "achievements": [
        "achievements",
        "awards",
        "honors"
    ],

    "summary": [
        "summary",
        "profile",
        "professional summary",
        "career objective"
    ]
}


def detect_sections(text):

    text_lower = text.lower()

    detected = {}

    for section, patterns in SECTION_PATTERNS.items():

        found = False

        for pattern in patterns:

            if re.search(
                r"\b"
                + re.escape(pattern)
                + r"\b",
                text_lower
            ):

                found = True
                break

        detected[section] = found

    return detected