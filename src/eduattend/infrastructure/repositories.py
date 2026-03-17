from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from ..domain.entities import Attendance
from ..domain.exceptions import DuplicateAttendanceError
from ..domain.ports import AttendanceRepository
from .models import AttendanceModel


class SqlAlchemyAttendanceRepository(AttendanceRepository):
    def __init__(self, session_factory) -> None:
        self._session_factory = session_factory

    def exists_for_student_class_day(
        self,
        student_id: str,
        course_id: str,
        class_session_id: str,
        attendance_date: date,
    ) -> bool:
        session = self._session_factory()
        try:
            statement = select(AttendanceModel.id).where(
                AttendanceModel.student_id == student_id,
                AttendanceModel.course_id == course_id,
                AttendanceModel.class_session_id == class_session_id,
                AttendanceModel.attendance_date == attendance_date,
            )
            return session.execute(statement).first() is not None
        finally:
            session.close()

    def save(self, attendance: Attendance) -> Attendance:
        session = self._session_factory()
        try:
            model = AttendanceModel(
                student_id=attendance.student_id,
                course_id=attendance.course_id,
                class_session_id=attendance.class_session_id,
                attendance_date=attendance.attendance_date,
                registered_at=attendance.registered_at,
            )
            session.add(model)
            session.commit()
            session.refresh(model)
            return Attendance(
                id=model.id,
                student_id=model.student_id,
                course_id=model.course_id,
                class_session_id=model.class_session_id,
                attendance_date=model.attendance_date,
                registered_at=model.registered_at,
            )
        except IntegrityError as exc:
            session.rollback()
            raise DuplicateAttendanceError(
                "El estudiante ya registró asistencia para esta clase en esta fecha."
            ) from exc
        finally:
            session.close()

    def list_all(self) -> list[Attendance]:
        session = self._session_factory()
        try:
            statement = select(AttendanceModel).order_by(AttendanceModel.registered_at.desc())
            rows = session.execute(statement).scalars().all()
            return [
                Attendance(
                    id=row.id,
                    student_id=row.student_id,
                    course_id=row.course_id,
                    class_session_id=row.class_session_id,
                    attendance_date=row.attendance_date,
                    registered_at=row.registered_at,
                )
                for row in rows
            ]
        finally:
            session.close()
