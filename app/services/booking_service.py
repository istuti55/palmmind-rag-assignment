
from app.database.db import SessionLocal
from app.database.models import Booking


def create_booking(
    name: str,
    email: str,
    interview_date,
    interview_time
) -> dict:
    db = SessionLocal()

    try:
        booking = Booking(
            name=name,
            email=email,
            interview_date=interview_date,
            interview_time=interview_time
        )

        db.add(booking)
        db.commit()
        db.refresh(booking)

        return {
            "id": booking.id,
            "name": booking.name,
            "email": booking.email,
            "interview_date": str(booking.interview_date),
            "interview_time": str(booking.interview_time)
        }

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()
