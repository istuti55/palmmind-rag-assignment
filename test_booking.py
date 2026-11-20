
from datetime import date, time
from app.services.booking_service import create_booking

booking = create_booking(
    name="Test Candidate",
    email="test@example.com",
    interview_date=date(2026, 12, 1),
    interview_time=time(10, 30)
)

print("Booking saved successfully!")
print(booking)
