# src/auth_service/domain/exception/auth_exceptions.py
class InvalidCredentialsError(Exception):
    pass


class TokenExpiredError(Exception):
    pass
