
import re
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

    existing_booking_id = redis_client.get(booking_key)

    # Get previous conversation
    history = get_chat_history(session_id)

    # If a booking already exists, check only the new message.
    if existing_booking_id:
        details = extract_booking_details(message)

        if not details.get("booking_intent"):
            return {
                "booking_intent": False,
                "booking_completed": False
            }

        return {
            "booking_intent": True,
            "booking_completed": True,
            "message": "Your interview has already been booked.",
            "booking_id": int(existing_booking_id)
        }

    # Continue an unfinished booking using conversation history
    conversation = "\n".join(
        history + [f"user: {message}"]
    )

    details = extract_booking_details(conversation)

    if not details.get("booking_intent"):
        return {
            "booking_intent": False,
            "booking_completed": False
        }

    save_message(session_id, "user", message)

    # Check for missing information
    required_fields = [
        "name",
        "email",
        "interview_date",
        "interview_time"
    ]

    missing_fields = [
        field for field in required_fields
        if not details.get(field)
        or not str(details[field]).strip()
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

    # Validate email
    email = details["email"].strip()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        reply = (
            "That email address doesn't look valid. "
            "Please provide a valid email address."
        )

        save_message(session_id, "assistant", reply)

        return {
            "booking_intent": True,
            "booking_completed": False,
            "message": reply,
            "invalid_fields": ["email"]
        }

    # Validate interview date
    try:
        interview_date = date.fromisoformat(
            details["interview_date"]
        )
    except (ValueError, TypeError):
        reply = "Please provide a valid interview date in YYYY-MM-DD format."

        save_message(session_id, "assistant", reply)

        return {
            "booking_intent": True,
            "booking_completed": False,
            "message": reply,
            "invalid_fields": ["interview_date"]
        }

    if interview_date < date.today():
        reply = "The interview date cannot be in the past. Please choose a future date."

        save_message(session_id, "assistant", reply)

        return {
            "booking_intent": True,
            "booking_completed": False,
            "message": reply,
            "invalid_fields": ["interview_date"]
        }

    # Validate interview time
    try:
        interview_time = time.fromisoformat(
            details["interview_time"]
        )
    except (ValueError, TypeError):
        reply = "Please provide a valid interview time, such as 10:30."

        save_message(session_id, "assistant", reply)

        return {
            "booking_intent": True,
            "booking_completed": False,
            "message": reply,
            "invalid_fields": ["interview_time"]
        }

    # Save booking in PostgreSQL
    booking = create_booking(
        name=details["name"].strip(),
        email=email,
        interview_date=interview_date,
        interview_time=interview_time
    )

    # Store booking ID in Redis for 30 days
    redis_client.set(
        booking_key,
        booking["id"],
        ex=30 * 24 * 60 * 60
    )

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
