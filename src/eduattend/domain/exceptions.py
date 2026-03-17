class BusinessRuleViolation(Exception):
    """Base exception for domain business rules."""


class DuplicateAttendanceError(BusinessRuleViolation):
    """Raised when attendance is registered more than once per class per day."""
