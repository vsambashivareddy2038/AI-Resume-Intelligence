class ResumeQualityAnalyzer:

    def analyze(
        self,
        text,
        sections
    ):

        score = 0

        feedback = []


        # Resume length

        word_count = len(
            text.split()
        )

        if word_count >= 250:

            score += 20

        else:

            feedback.append(
                "Resume contains limited content."
            )


        # Education

        if sections.get("education"):

            score += 15

        else:

            feedback.append(
                "Add an Education section."
            )


        # Skills

        if sections.get("skills"):

            score += 20

        else:

            feedback.append(
                "Add a Technical Skills section."
            )


        # Projects

        if sections.get("projects"):

            score += 20

        else:

            feedback.append(
                "Add relevant projects."
            )


        # Experience

        if sections.get("experience"):

            score += 15

        else:

            feedback.append(
                "Add internship or work experience "
                "if applicable."
            )


        # Certifications

        if sections.get("certifications"):

            score += 10

        else:

            feedback.append(
                "Add relevant certifications if available."
            )


        return {

            "score": min(score, 100),

            "feedback": feedback

        }