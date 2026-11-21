
import os
import json
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.5-flash-lite"


def generate_answer(question: str, context: str) -> str:
    """Generate an answer using retrieved document context."""

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


def extract_booking_details(conversation: str) -> dict:
    """Extract interview booking details from conversation."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an interview booking assistant.

    Return ONLY a valid JSON object with these fields:

    {{
        "booking_intent": true,
        "name": null,
        "email": null,
        "interview_date": null,
        "interview_time": null,
        "missing_fields": [],
        "reply": "A friendly message"
    }}

    Instructions:
    1. Detect whether the candidate wants to book an interview.
    2. Extract name, email, date and time.
    3. Never invent missing information.
    4. Ask for missing details one at a time.
    5. Use the entire conversation.
    6. Return dates in YYYY-MM-DD format.
    7. If the user provides a time, extract it even if it is invalid.
    8. For valid times, return them in 24-hour HH:MM format.
    9. For invalid times, preserve the original value so the application can validate it.
    10. Never set a provided time to null just because its format is invalid.

    Conversation:
    {conversation}
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty response")

    raw_response = response.text.strip()

    # Remove Markdown code fences if Gemini adds them
    if raw_response.startswith("```"):
        raw_response = raw_response.split("\n", 1)[1]

        if raw_response.endswith("```"):
            raw_response = raw_response[:-3].strip()

    try:
        return json.loads(raw_response)

    except json.JSONDecodeError as error:
        raise ValueError(
            f"Gemini returned invalid JSON: {raw_response}"
        ) from error


def evaluate_answer(expected_answer: str, actual_answer: str) -> bool:
    """Evaluate whether two answers have the same meaning using Gemini."""

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")

    client = genai.Client(api_key=api_key)

    prompt = f"""
    You are an answer quality evaluator.

    Compare the expected answer with the actual answer.

    Consider the answers equivalent if they communicate
    the same important information, even when the wording differs.

    Do not require exact word matching.
    Mark the answer incorrect if it contains contradictory
    or materially incorrect information.

    Expected answer:
    {expected_answer}

    Actual answer:
    {actual_answer}

    Return ONLY YES or NO.
    """

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt
    )

    if not response.text:
        raise ValueError("Gemini returned an empty evaluation")

    return response.text.strip().upper() == "YES"
