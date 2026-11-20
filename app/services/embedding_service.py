
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-embedding-001"


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Convert a list of text chunks into numerical embeddings.
    """

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    if not texts or any(not text.strip() for text in texts):
        raise ValueError("Texts cannot be empty")

    client = genai.Client(api_key=api_key)

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=texts,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT",
            output_dimensionality=768
        )
    )

    return [
        embedding.values
        for embedding in response.embeddings
    ]


def generate_query_embedding(question: str) -> list[float]:
    """
    Convert a user's question into an embedding for searching Qdrant.
    """
    if not question.strip():
        raise ValueError("Question cannot be empty")

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    client = genai.Client(api_key=api_key)

    response = client.models.embed_content(
        model=MODEL_NAME,
        contents=question,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_QUERY",
            output_dimensionality=768
        )
    )

    return response.embeddings[0].values
