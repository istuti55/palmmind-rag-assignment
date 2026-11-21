
from datetime import date, timedelta

import pytest

from app.services import interview_service


@pytest.fixture
def mock_dependencies(monkeypatch):
    monkeypatch.setattr(
        interview_service.redis_client,
        "get",
        lambda key: None
    )

    monkeypatch.setattr(
        interview_service.redis_client,
        "set",
        lambda *args, **kwargs: True
    )

    monkeypatch.setattr(
        interview_service,
        "get_chat_history",
        lambda session_id: []
    )

    monkeypatch.setattr(
        interview_service,
        "save_message",
        lambda *args: None
    )


def valid_details():
    return {
        "booking_intent": True,
        "name": "John Smith",
        "email": "john@example.com",
        "interview_date": (
            date.today() + timedelta(days=7)
        ).isoformat(),
        "interview_time": "10:30"
    }


def test_empty_message():
    with pytest.raises(ValueError, match="Message cannot be empty"):
        interview_service.process_interview_message(
            "test", "   "
        )


def test_already_completed_booking(monkeypatch):
    monkeypatch.setattr(
        interview_service.redis_client,
        "get",
        lambda key: "42"
    )

    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda message: {"booking_intent": True}
    )

    result = interview_service.process_interview_message(
        "test_session", "Book my interview"
    )

    assert result["booking_completed"] is True
    assert result["booking_id"] == 42


def test_no_booking_intent(monkeypatch, mock_dependencies):
    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: {"booking_intent": False}
    )

    result = interview_service.process_interview_message(
        "test_session", "Hello"
    )

    assert result["booking_intent"] is False
    assert result["booking_completed"] is False


def test_missing_booking_details(monkeypatch, mock_dependencies):
    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: {
            "booking_intent": True,
            "name": "John Smith",
            "reply": "Please provide your email."
        }
    )

    result = interview_service.process_interview_message(
        "test_session", "I want to book"
    )

    assert result["booking_completed"] is False
    assert "email" in result["missing_fields"]


def test_invalid_email(monkeypatch, mock_dependencies):
    details = valid_details()
    details["email"] = "invalid-email"

    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: details
    )

    result = interview_service.process_interview_message(
        "test_session", "Book my interview"
    )

    assert result["booking_completed"] is False
    assert result["invalid_fields"] == ["email"]


def test_invalid_interview_date(monkeypatch, mock_dependencies):
    details = valid_details()
    details["interview_date"] = "not-a-date"

    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: details
    )

    result = interview_service.process_interview_message(
        "test_session", "Book my interview"
    )

    assert result["invalid_fields"] == ["interview_date"]


def test_past_interview_date(monkeypatch, mock_dependencies):
    details = valid_details()
    details["interview_date"] = (
        date.today() - timedelta(days=1)
    ).isoformat()

    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: details
    )

    result = interview_service.process_interview_message(
        "test_session", "Book my interview"
    )

    assert result["invalid_fields"] == ["interview_date"]


def test_invalid_interview_time(monkeypatch, mock_dependencies):
    details = valid_details()
    details["interview_time"] = "invalid-time"

    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: details
    )

    result = interview_service.process_interview_message(
        "test_session", "Book my interview"
    )

    assert result["invalid_fields"] == ["interview_time"]


def test_successful_booking(monkeypatch, mock_dependencies):
    details = valid_details()

    booking = {
        "id": 101,
        "name": "John Smith",
        "email": "john@example.com",
        "interview_date": details["interview_date"],
        "interview_time": "10:30"
    }

    monkeypatch.setattr(
        interview_service,
        "extract_booking_details",
        lambda conversation: details
    )

    monkeypatch.setattr(
        interview_service,
        "create_booking",
        lambda **kwargs: booking
    )

    result = interview_service.process_interview_message(
        "test_session", "Book my interview"
    )

    assert result["booking_completed"] is True
    assert result["booking"]["id"] == 101
    assert "successfully" in result["message"]
