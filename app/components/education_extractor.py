import re


class EducationExtractor:

    """
    Extract education-related information
    from resume text.
    """

    DEGREE_PATTERNS = {

        "B.Tech": [
            r"\bb\.?\s*tech\b",
            r"\bbachelor\s+of\s+technology\b"
        ],

        "B.E": [
            r"\bb\.?\s*e\b",
            r"\bbachelor\s+of\s+engineering\b"
        ],

        "B.Sc": [
            r"\bb\.?\s*sc\b",
            r"\bbachelor\s+of\s+science\b"
        ],

        "BCA": [
            r"\bbca\b",
            r"\bbachelor\s+of\s+computer\s+applications\b"
        ],

        "M.Tech": [
            r"\bm\.?\s*tech\b",
            r"\bmaster\s+of\s+technology\b"
        ],

        "M.E": [
            r"\bm\.?\s*e\b",
            r"\bmaster\s+of\s+engineering\b"
        ],

        "M.Sc": [
            r"\bm\.?\s*sc\b",
            r"\bmaster\s+of\s+science\b"
        ],

        "MCA": [
            r"\bmca\b",
            r"\bmaster\s+of\s+computer\s+applications\b"
        ],

        "MBA": [
            r"\bmba\b",
            r"\bmaster\s+of\s+business\s+administration\b"
        ],

        "Ph.D": [
            r"\bph\.?\s*d\b",
            r"\bdoctor\s+of\s+philosophy\b"
        ],

        "Intermediate": [
            r"\bintermediate\b",
            r"\b12th\b",
            r"\bhigher\s+secondary\b"
        ],

        "SSC": [
            r"\bssc\b",
            r"\b10th\b",
            r"\bsecondary\s+school\b"
        ]
    }


    SPECIALIZATION_KEYWORDS = [

        "computer science",

        "computer science and engineering",

        "cse",

        "artificial intelligence",

        "machine learning",

        "ai & ml",

        "ai/ml",

        "information technology",

        "it",

        "electronics and communication",

        "ece",

        "electrical and electronics",

        "eee",

        "mechanical engineering",

        "civil engineering",

        "data science",

        "cyber security",

        "cybersecurity"

    ]


    def extract_degree(self, text):

        """
        Identify the highest-level degree mentioned
        in the resume.
        """

        text_lower = text.lower()

        for degree, patterns in self.DEGREE_PATTERNS.items():

            for pattern in patterns:

                if re.search(
                    pattern,
                    text_lower
                ):

                    return degree

        return None


    def extract_all_degrees(self, text):

        """
        Extract every education qualification
        mentioned in the resume.
        """

        text_lower = text.lower()

        degrees = []

        for degree, patterns in self.DEGREE_PATTERNS.items():

            for pattern in patterns:

                if re.search(
                    pattern,
                    text_lower
                ):

                    degrees.append(degree)

                    break

        return degrees


    def extract_specialization(self, text):

        """
        Detect branch or specialization.
        """

        text_lower = text.lower()

        # Check longer phrases first
        # so that "computer science and engineering"
        # is preferred over "computer science".

        keywords = sorted(
            self.SPECIALIZATION_KEYWORDS,
            key=len,
            reverse=True
        )

        for keyword in keywords:

            if re.search(
                r"\b"
                + re.escape(keyword)
                + r"\b",
                text_lower
            ):

                return keyword

        return None


    def extract_graduation_year(self, text):

        """
        Extract likely graduation year.

        Looks for years between 2000 and 2099.
        """

        years = re.findall(
            r"\b(20\d{2})\b",
            text
        )

        if not years:

            return None

        # If a range exists such as
        # 2024 - 2028, prefer the final year.

        range_pattern = (
            r"\b(20\d{2})\s*"
            r"(?:-|–|—|to)\s*"
            r"(20\d{2})\b"
        )

        ranges = re.findall(
            range_pattern,
            text,
            re.IGNORECASE
        )

        if ranges:

            return ranges[0][1]

        # Otherwise return the last year found.

        return years[-1]


    def extract_institution(self, text):

        """
        Attempt to identify the educational institution.

        Uses lines containing common educational
        institution keywords.
        """

        lines = text.splitlines()

        institution_keywords = [

            "university",

            "college",

            "institute",

            "school",

            "academy",

            "education"

        ]

        for line in lines:

            line = line.strip()

            if not line:

                continue

            lower_line = line.lower()

            for keyword in institution_keywords:

                if keyword in lower_line:

                    # Avoid returning a generic section
                    # heading such as "Education".

                    if lower_line.strip() in [
                        "education",
                        "academic background",
                        "educational background"
                    ]:

                        continue

                    return line

        return None


    def extract(self, text):

        """
        Extract complete education information.
        """

        return {

            "degree":
                self.extract_degree(text),

            "degrees":
                self.extract_all_degrees(text),

            "institution":
                self.extract_institution(text),

            "specialization":
                self.extract_specialization(text),

            "graduation_year":
                self.extract_graduation_year(text)

        }

