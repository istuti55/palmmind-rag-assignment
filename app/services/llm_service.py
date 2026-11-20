
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.1-flash-lite"


def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer using the question and retrieved document context.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    if not question.strip():
        raise ValueError("Question cannot be empty")

    if not context.strip():
        raise ValueError("Context cannot be empty")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are a helpful document assistant.

    Answer the user's question using only the information
    provided in the context.

    If the answer is not available in the context,
    say that the document does not contain this information.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    return response.text
