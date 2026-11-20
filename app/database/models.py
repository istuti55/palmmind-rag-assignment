
from datetime import date, time, datetime

from sqlalchemy import Column, Integer, String, Date, Time, DateTime
from app.database.db import Base


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    interview_date = Column(Date, nullable=False)
    interview_time = Column(Time, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
