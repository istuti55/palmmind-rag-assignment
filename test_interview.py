
from app.services.interview_service import process_interview_message
from app.services.redis_service import redis_client

# Clear old test conversation
redis_client.delete("chat:interview_test")
redis_client.delete("booking_completed:interview_test")

session_id = "interview_test"

messages = [
    "I want to book an interview.",
    "My name is John Smith.",
    "My email is john@example.com.",
    "I want December 1, 2026.",
    "10:30 AM."
]

for message in messages:
    print("\nCandidate:", message)

    result = process_interview_message(
        session_id=session_id,
        message=message
    )

    print("Chatbot:", result)
