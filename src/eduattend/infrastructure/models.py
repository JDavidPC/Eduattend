from sqlalchemy import Date, DateTime, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .db import Base


class AttendanceModel(Base):
    __tablename__ = "attendances"
    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            "class_session_id",
            "attendance_date",
            name="uq_attendance_student_class_day",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[str] = mapped_column(String(50), nullable=False)
    course_id: Mapped[str] = mapped_column(String(50), nullable=False)
    class_session_id: Mapped[str] = mapped_column(String(50), nullable=False)
    attendance_date: Mapped[Date] = mapped_column(Date, nullable=False)
    registered_at: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
