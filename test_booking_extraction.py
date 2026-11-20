
from app.services.llm_service import extract_booking_details

conversation = """
Candidate: I want to book an interview.
Candidate: My name is John Smith.
Candidate: My email is john@example.com.
Candidate: I want the interview on December 1, 2026.
Candidate: 10:30 AM.
"""

result = extract_booking_details(conversation)

print("Booking extraction result:")
print(result)
