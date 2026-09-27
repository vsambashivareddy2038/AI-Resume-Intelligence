class ATSScorer:


    # Calculate the percentage of required skills found.
    def calculate_skill_match(
        self,
        resume_skills,
        required_skills
    ):
        resume_set = {
            skill.lower()
            for skill in resume_skills
        }

        required_set = {
            skill.lower()
            for skill in required_skills
        }

        if not required_set:
            return 0.0

        matched = resume_set & required_set

        score = (
            len(matched)
            / len(required_set)
        ) * 100

        return round(score, 2)


    # Return skills that exist in both lists.
    def matched_skills(
        self,
        resume_skills,
        required_skills
    ):
        resume_set = {
            skill.lower()
            for skill in resume_skills
        }

        return [
            skill
            for skill in required_skills
            if skill.lower() in resume_set
        ]


    # Return required skills missing from the resume.
    def missing_skills(
        self,
        resume_skills,
        required_skills
    ):
        resume_set = {
            skill.lower()
            for skill in resume_skills
        }

        return [
            skill
            for skill in required_skills
            if skill.lower() not in resume_set
        ]


    # Score the candidate's overall experience.
    def calculate_experience_score(
        self,
        experience
    ):
        if not experience:
            return 0.0

        total_months = experience.get(
            "total_experience_months",
            0
        )

        try:
            total_months = float(
                total_months
            )
        except (
            TypeError,
            ValueError
        ):
            total_months = 0.0

        if total_months <= 0:
            return 0.0

        if total_months < 6:
            return 50.0

        if total_months < 12:
            return 60.0

        if total_months < 24:
            return 70.0

        if total_months < 36:
            return 80.0

        if total_months < 60:
            return 90.0

        return 100.0


    # Compare candidate experience with the job requirement.
    def calculate_requirement_experience_score(
        self,
        resume_experience,
        experience_requirement
    ):
        if not experience_requirement:
            return 0.0

        required = experience_requirement.get(
            "experience_required",
            False
        )

        if not required:
            return 100.0

        min_years = experience_requirement.get(
            "min_years",
            0.0
        )

        max_years = experience_requirement.get(
            "max_years"
        )

        try:
            min_years = float(
                min_years
            )
        except (
            TypeError,
            ValueError
        ):
            min_years = 0.0

        resume_years = 0.0

        if resume_experience:
            resume_years = resume_experience.get(
                "total_experience_years",
                0.0
            )

        try:
            resume_years = float(
                resume_years
            )
        except (
            TypeError,
            ValueError
        ):
            resume_years = 0.0

        if min_years <= 0:
            if max_years is not None:
                try:
                    max_years = float(
                        max_years
                    )

                    if resume_years <= max_years:
                        return 100.0

                    return 90.0

                except (
                    TypeError,
                    ValueError
                ):
                    pass

            return 100.0

        if resume_years >= min_years:

            if max_years is not None:

                try:
                    max_years = float(
                        max_years
                    )

                    if resume_years <= max_years:
                        return 100.0

                    return 90.0

                except (
                    TypeError,
                    ValueError
                ):
                    pass

            return 100.0

        score = (
            resume_years
            / min_years
        ) * 100

        return round(
            min(
                max(score, 0.0),
                99.0
            ),
            2
        )


    # Score the basic education details.
    def calculate_education_score(
        self,
        education
    ):
        if not education:
            return 0.0

        score = 0.0

        degree = education.get(
            "degree"
        )

        degrees = education.get(
            "degrees",
            []
        )

        has_degree = bool(
            degree
            or degrees
        )

        if has_degree:
            score += 50.0

        institution = education.get(
            "institution"
        )

        if institution:
            score += 20.0

        specialization = education.get(
            "specialization"
        )

        if specialization:
            score += 15.0

        graduation_year = education.get(
            "graduation_year"
        )

        if graduation_year:
            score += 15.0

        return min(
            round(score, 2),
            100.0
        )


    # Normalize degree names before comparison.
    def _normalize_degree_level(
        self,
        degree
    ):

        if not degree:
            return ""

        degree = str(
            degree
        ).lower().strip()

        normalized = (
            degree
            .replace(".", "")
            .replace("-", "")
            .replace(" ", "")
        )


        bachelor_degrees = {
            "btech",
            "be",
            "bsc",
            "bca",
            "bcs",
            "bba",
            "bcom",
            "bachelor",
            "bachelors",
            "bacheloroftechnology",
            "bachelorofengineering",
            "bachelorofscience",
            "bachelorofcomputerapplications"
        }

        if normalized in bachelor_degrees:
            return "bachelor"


        master_degrees = {
            "mtech",
            "me",
            "msc",
            "mca",
            "mba",
            "mcs",
            "master",
            "masters",
            "masteroftechnology",
            "masterofengineering",
            "masterofscience",
            "masterofcomputerapplications"
        }

        if normalized in master_degrees:
            return "master"


        doctorate_degrees = {
            "phd",
            "doctorate",
            "doctoral",
            "doctorofphilosophy"
        }

        if normalized in doctorate_degrees:
            return "doctorate"


        diploma_degrees = {
            "diploma",
            "polytechnic"
        }

        if normalized in diploma_degrees:
            return "diploma"


        intermediate_degrees = {
            "intermediate",
            "12th",
            "class12",
            "hsc"
        }

        if normalized in intermediate_degrees:
            return "intermediate"


        school_degrees = {
            "ssc",
            "10th",
            "class10",
            "matriculation"
        }

        if normalized in school_degrees:
            return "school"

        return normalized


    # Compare resume education with job requirements.
    def calculate_requirement_education_score(
        self,
        resume_education,
        education_requirement
    ):


        if not education_requirement:
            return 0.0

        required_degree = (
            education_requirement.get(
                "degree_level"
            )
        )

        required_fields = (
            education_requirement.get(
                "fields",
                []
            )
        )

        if (
            not required_degree
            and not required_fields
        ):
            return 100.0


        if not resume_education:
            return 0.0

        score = 0.0


        resume_degrees = []

        degree = resume_education.get(
            "degree"
        )

        if degree:
            resume_degrees.append(
                degree
            )

        degrees = resume_education.get(
            "degrees",
            []
        )

        if degrees:
            resume_degrees.extend(
                degrees
            )

        unique_degrees = []

        seen = set()

        for item in resume_degrees:

            normalized_item = str(
                item
            ).strip().lower()

            if normalized_item not in seen:

                seen.add(
                    normalized_item
                )

                unique_degrees.append(
                    item
                )


        degree_match = False

        if required_degree:

            normalized_required_degree = (
                self._normalize_degree_level(
                    required_degree
                )
            )

            for resume_degree in unique_degrees:

                normalized_resume_degree = (
                    self._normalize_degree_level(
                        resume_degree
                    )
                )

                if (
                    normalized_resume_degree
                    == normalized_required_degree
                ):
                    degree_match = True
                    break

                if (
                    normalized_required_degree
                    in normalized_resume_degree
                ):
                    degree_match = True
                    break

        if degree_match:
            score += 60.0


        resume_specialization = str(
            resume_education.get(
                "specialization",
                ""
            )
        ).lower()

        field_match = False

        for field in required_fields:

            field = str(
                field
            ).lower().strip()

            if not field:
                continue

            if field in resume_specialization:
                field_match = True
                break

        if field_match:
            score += 40.0


        if (
            not required_fields
            and degree_match
        ):
            score = 100.0

        return min(
            round(score, 2),
            100.0
        )


    # Score the resume structure.
    def calculate_structure_score(
        self,
        sections
    ):
        if not sections:
            return 0.0

        section_weights = {
            "education": 20,
            "skills": 20,
            "projects": 20,
            "experience": 15,
            "certifications": 10,
            "achievements": 10,
            "summary": 5
        }

        score = 0.0

        for section, weight in (
            section_weights.items()
        ):

            if sections.get(
                section,
                False
            ):
                score += weight

        return round(
            score,
            2
        )


    # Calculate the original ATS score.
    def overall_score(
        self,
        skill_score,
        semantic_score,
        experience_score,
        education_score,
        structure_score
    ):
        score = (
            skill_score * 0.40
            + semantic_score * 0.30
            + experience_score * 0.15
            + education_score * 0.10
            + structure_score * 0.05
        )

        return round(
            score,
            2
        )


    # Calculate the requirement-aware ATS score.
    def requirement_aware_score(
        self,
        skill_score,
        preferred_skill_score,
        semantic_score,
        experience_requirement_score,
        education_requirement_score,
        structure_score
    ):
        score = (
            skill_score * 0.35
            + semantic_score * 0.25
            + experience_requirement_score * 0.15
            + education_requirement_score * 0.10
            + preferred_skill_score * 0.10
            + structure_score * 0.05
        )

        return round(
            score,
            2
        )