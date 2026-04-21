from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class UpdateAttendanceCommand:
    student_id: str
    course_id: str
    class_session_id: str
    attendance_date: date
