import re
from datetime import datetime

class ExperienceExtractor:
    MONTHS = {
        "january": 1,
        "february": 2,
        "march": 3,
        "april": 4,
        "may": 5,
        "june": 6,
        "july": 7,
        "august": 8,
        "september": 9,
        "october": 10,
        "november": 11,
        "december": 12,
    }

    MONTH_ABBREVIATIONS = {
        "jan": "january",
        "feb": "february",
        "mar": "march",
        "apr": "april",
        "jun": "june",
        "jul": "july",
        "aug": "august",
        "sep": "september",
        "sept": "september",
        "oct": "october",
        "nov": "november",
        "dec": "december",
    }

    EXPERIENCE_HEADINGS = {
        "experience",
        "work experience",
        "professional experience",
        "employment",
        "work history",
        "internship",
        "internships",
        "career history",
    }

    STOP_HEADINGS = {
        "education",
        "projects",
        "skills",
        "technical skills",
        "certifications",
        "certificates",
        "achievements",
        "awards",
        "summary",
        "profile",
        "career objective",
        "objective",
        "languages",
        "hobbies",
        "interests",
        "references",
    }

    JOB_TITLE_KEYWORDS = [
        "intern",
        "developer",
        "engineer",
        "scientist",
        "analyst",
        "manager",
        "designer",
        "consultant",
        "administrator",
        "architect",
        "specialist",
        "associate",
        "lead",
        "researcher",
        "trainee",
        "executive",
        "officer",
        "programmer",
        "technician",
        "devops",
        "mlops",
    ]

    COMPANY_INDICATORS = [
        "technologies",
        "technology",
        "solutions",
        "systems",
        "services",
        "private limited",
        "pvt ltd",
        "limited",
        "ltd",
        "inc",
        "corp",
        "corporation",
        "company",
        "labs",
        "laboratories",
        "consulting",
        "industries",
        "enterprises",
        "group",
    ]

    def __init__(self):
        pass

    def _clean_line(self, line):
        line = line.strip()

        line = re.sub(
            r"^[•●▪◦*-]\s*",
            "",
            line
        )

        return line.strip()

    def _is_stop_heading(self, line):
        return (
            self._clean_line(line).lower()
            in self.STOP_HEADINGS
        )

    def _is_date_line(self, line):
        text = self._clean_line(line).lower()

        month_names = (
            r"(?:"
            r"january|february|march|april|may|june|july|"
            r"august|september|october|november|december|"
            r"jan|feb|mar|apr|jun|jul|aug|sep|sept|oct|nov|dec"
            r")"
        )

        month_year = rf"{month_names}\s+\d{{4}}"

        patterns = [
            rf"{month_year}\s*[-–—]\s*{month_year}",
            rf"{month_year}\s*[-–—]\s*(?:present|current)",
            r"\d{1,2}/\d{4}\s*[-–—]\s*\d{1,2}/\d{4}",
            r"\d{1,2}/\d{4}\s*[-–—]\s*(?:present|current)",
            r"\d{4}\s*[-–—]\s*\d{4}",
            r"\d{4}\s*[-–—]\s*(?:present|current)",
        ]

        return any(
            re.fullmatch(pattern, text)
            for pattern in patterns
        )

    def _extract_date_range(self, line):
        text = self._clean_line(line)

        text = text.replace("–", "-")
        text = text.replace("—", "-")

        parts = re.split(
            r"\s*-\s*",
            text
        )

        if len(parts) != 2:
            return None, None

        return (
            parts[0].strip(),
            parts[1].strip()
        )

    def _normalize_month(self, month):
        month = month.lower().strip()

        return self.MONTH_ABBREVIATIONS.get(
            month,
            month
        )

    def _parse_date(self, value):
        if not value:
            return None, None

        value = value.strip().lower()

        if value in {"present", "current"}:
            now = datetime.now()
            return now.year, now.month

        match = re.fullmatch(
            r"([a-z]+)\s+(\d{4})",
            value
        )

        if match:
            month_name = self._normalize_month(
                match.group(1)
            )

            year = int(match.group(2))

            month = self.MONTHS.get(
                month_name
            )

            if month:
                return year, month

        match = re.fullmatch(
            r"(\d{1,2})/(\d{4})",
            value
        )

        if match:
            month = int(match.group(1))
            year = int(match.group(2))

            if 1 <= month <= 12:
                return year, month

        match = re.fullmatch(
            r"\d{4}",
            value
        )

        if match:
            return int(value), 1

        return None, None

    def _format_date(self, value):
        year, month = self._parse_date(value)

        if year is None or month is None:
            return value.strip() if value else ""

        month_name = list(
            self.MONTHS.keys()
        )[month - 1]

        return f"{month_name.capitalize()} {year}"

    def _calculate_duration_months(
        self,
        start_date,
        end_date
    ):
        start_year, start_month = self._parse_date(
            start_date
        )

        end_year, end_month = self._parse_date(
            end_date
        )

        if None in (
            start_year,
            start_month,
            end_year,
            end_month
        ):
            return 0

        duration = (
            (end_year - start_year) * 12
            + (end_month - start_month)
        )

        return max(duration, 1)

    def _looks_like_job_title(self, line):
        text = self._clean_line(line)

        if not text:
            return False

        lower = text.lower()

        if self._is_date_line(text):
            return False

        if self._is_stop_heading(text):
            return False

        # job titles when they contain strong company indicators.
        for indicator in self.COMPANY_INDICATORS:
            if indicator in lower:
                return False

        if len(text.split()) > 8:
            return False

        description_starters = [
            "developed ",
            "worked ",
            "responsible ",
            "created ",
            "built ",
            "designed ",
            "implemented ",
            "analyzed ",
            "cleaned ",
            "managed ",
            "assisted ",
            "using ",
            "used ",
            "experience ",
            "developing ",
            "working ",
            "performed ",
            "supported ",
        ]

        if any(
            lower.startswith(prefix)
            for prefix in description_starters
        ):
            return False

        for keyword in self.JOB_TITLE_KEYWORDS:
            if keyword in lower:
                return True

        # Title Case fallback.
        words = text.split()

        if 1 <= len(words) <= 6:

            capitalized_count = sum(
                1
                for word in words
                if word[:1].isupper()
            )

            if capitalized_count == len(words):
                return True

        return False

    def _extract_pipe_format(self, line):
        if "|" not in line:
            return None, None

        parts = [
            part.strip()
            for part in line.split("|")
        ]

        if len(parts) < 2:
            return None, None

        title = parts[0]
        company = parts[1]

        if self._looks_like_job_title(title):
            return title, company

        return None, None

    def _collect_description(
        self,
        lines,
        start_index
    ):
        description = []

        for i in range(
            start_index,
            len(lines)
        ):
            line = lines[i]

            if self._is_stop_heading(line):
                break

            if self._is_date_line(line):
                break

            # A new strong job title means a new entry.
            if self._looks_like_job_title(line):
                break

            description.append(line)

        return " ".join(description).strip()

    def _detect_experience_type(self, title):
        lower = title.lower()

        if "intern" in lower:
            return "Internship"

        if "trainee" in lower:
            return "Trainee"

        if "freelance" in lower:
            return "Freelance"

        if "contract" in lower:
            return "Contract"

        return "Full-time"

    def extract(self, text):

        if not text or not text.strip():
            return {
                "entries": [],
                "total_experience_months": 0,
                "total_experience_years": 0.0,
            }

        raw_lines = text.splitlines()

        lines = []

        for line in raw_lines:
            cleaned = self._clean_line(line)

            if cleaned:
                lines.append(cleaned)

        start_index = None

        for index, line in enumerate(lines):

            if (
                line.lower()
                in self.EXPERIENCE_HEADINGS
            ):
                start_index = index + 1
                break

        if start_index is None:
            return {
                "entries": [],
                "total_experience_months": 0,
                "total_experience_years": 0.0,
            }

        experience_lines = []

        for line in lines[start_index:]:

            if self._is_stop_heading(line):
                break

            experience_lines.append(line)

        entries = []

        i = 0

        while i < len(experience_lines):

            current = experience_lines[i]

            # DATA SCIENCE INTERN | ABC Technologies
            # Dec 2025 - Mar 2026

            title, company = self._extract_pipe_format(
                current
            )

            if title:

                if (
                    i + 1 < len(experience_lines)
                    and self._is_date_line(
                        experience_lines[i + 1]
                    )
                ):

                    date_line = experience_lines[
                        i + 1
                    ]

                    start_date, end_date = (
                        self._extract_date_range(
                            date_line
                        )
                    )

                    duration = (
                        self._calculate_duration_months(
                            start_date,
                            end_date
                        )
                    )

                    description = (
                        self._collect_description(
                            experience_lines,
                            i + 2
                        )
                    )

                    entries.append({
                        "title": title,
                        "company": company,
                        "start_date": self._format_date(
                            start_date
                        ),
                        "end_date": self._format_date(
                            end_date
                        ),
                        "duration_months": duration,
                        "type": self._detect_experience_type(
                            title
                        ),
                        "description": description,
                    })

                    i += 2
                    continue

            # Machine Learning Intern
            # ABC Technologies
            # June 2025 - August 2025

            if self._looks_like_job_title(current):

                title = current

                # If the next line is followed by a date line,
                # that next line MUST be the company.
                # This prevents:
                # Machine Learning Intern
                # ABC Technologies
                # June 2025 - August 2025
                # from becoming:
                # title = ABC Technologies

                if (
                    i + 2 < len(experience_lines)
                    and self._is_date_line(
                        experience_lines[i + 2]
                    )
                ):

                    company = experience_lines[
                        i + 1
                    ]

                    date_index = i + 2

                # Machine Learning Intern
                # June 2025 - August 2025

                elif (
                    i + 1 < len(experience_lines)
                    and self._is_date_line(
                        experience_lines[i + 1]
                    )
                ):

                    company = ""

                    date_index = i + 1

                else:
                    i += 1
                    continue

                date_line = experience_lines[
                    date_index
                ]

                start_date, end_date = (
                    self._extract_date_range(
                        date_line
                    )
                )

                duration = (
                    self._calculate_duration_months(
                        start_date,
                        end_date
                    )
                )

                description = (
                    self._collect_description(
                        experience_lines,
                        date_index + 1
                    )
                )

                entries.append({
                    "title": title,
                    "company": company,
                    "start_date": self._format_date(
                        start_date
                    ),
                    "end_date": self._format_date(
                        end_date
                    ),
                    "duration_months": duration,
                    "type": self._detect_experience_type(
                        title
                    ),
                    "description": description,
                })

                i = date_index + 1
                continue

            i += 1

        total_months = sum(
            entry.get(
                "duration_months",
                0
            )
            for entry in entries
        )

        total_years = round(
            total_months / 12,
            2
        )

        return {
            "entries": entries,
            "total_experience_months": total_months,
            "total_experience_years": total_years,
        }
