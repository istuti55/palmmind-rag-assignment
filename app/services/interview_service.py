
from datetime import date, time

from app.services.llm_service import extract_booking_details
from app.services.booking_service import create_booking
from app.services.redis_service import (
    save_message,
    get_chat_history,
    redis_client
)


def process_interview_message(session_id: str, message: str) -> dict:
    """Process an interview booking conversation."""

    if not message.strip():
        raise ValueError("Message cannot be empty")

    booking_key = f"booking_completed:{session_id}"

    # Check whether this session already has a completed booking
    existing_booking_id = redis_client.get(booking_key)

    if existing_booking_id:
        return {
            "booking_intent": True,
            "booking_completed": True,
            "message": "Your interview has already been booked.",
            "booking_id": int(existing_booking_id)
        }

    # Get previous conversation
    history = get_chat_history(session_id)

    # Include the current message without saving it yet
    conversation = "\n".join(
        history + [f"user: {message}"]
    )

    # Ask Gemini to identify booking intent and extract details
    details = extract_booking_details(conversation)

    if not details.get("booking_intent"):
        return {
            "booking_intent": False,
            "booking_completed": False
        }

    # Save the message only when it is part of a booking conversation
    save_message(session_id, "user", message)

    # Calculate missing fields in Python
    required_fields = [
        "name",
        "email",
        "interview_date",
        "interview_time"
    ]

    missing_fields = [
        field for field in required_fields
        if not details.get(field)
    ]

    if missing_fields:
        reply = details.get(
            "reply",
            "Please provide the missing interview details."
        )

        save_message(session_id, "assistant", reply)

        return {
            "booking_intent": True,
            "booking_completed": False,
            "message": reply,
            "missing_fields": missing_fields
        }

    # Convert date and time strings into Python objects
    interview_date = date.fromisoformat(details["interview_date"])
    interview_time = time.fromisoformat(details["interview_time"])

    # Save booking in PostgreSQL
    booking = create_booking(
        name=details["name"],
        email=details["email"],
        interview_date=interview_date,
        interview_time=interview_time
    )

    # Remember completed booking in Redis
    redis_client.set(booking_key, booking["id"])

    reply = (
        f"Your interview has been booked successfully, "
        f"{booking['name']}! "
        f"Date: {booking['interview_date']}. "
        f"Time: {booking['interview_time']}. "
        f"Booking ID: {booking['id']}."
    )

    save_message(session_id, "assistant", reply)

    return {
        "booking_intent": True,
        "booking_completed": True,
        "message": reply,
        "booking": booking
    }
