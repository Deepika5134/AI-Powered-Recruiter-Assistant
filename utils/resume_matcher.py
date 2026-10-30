from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load the AI model
model = SentenceTransformer("all-MiniLM-L6-v2")


def calculate_semantic_similarity(
    resume_text,
    job_description
):
    """
    Compare the meaning of a resume and
    a job description using Sentence Transformers.
    """

    resume_embedding = model.encode(
        [resume_text]
    )

    job_embedding = model.encode(
        [job_description]
    )

    similarity = cosine_similarity(
        resume_embedding,
        job_embedding
    )[0][0]

    score = float(similarity * 100)
    return round(score, 2)