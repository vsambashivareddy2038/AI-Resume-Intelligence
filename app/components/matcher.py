from sentence_transformers import (
    SentenceTransformer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


class SemanticMatcher:

    def __init__(self):

        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )


    def calculate_similarity(
        self,
        resume_text,
        job_description
    ):

        embeddings = self.model.encode(
            [
                resume_text,
                job_description
            ]
        )

        similarity = cosine_similarity(
            [
                embeddings[0]
            ],
            [
                embeddings[1]
            ]
        )[0][0]

        return round(
            float(similarity * 100),
            2
        )