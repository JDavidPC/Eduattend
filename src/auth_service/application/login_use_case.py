# src/auth_service/application/login_use_case.py
from ..domain.service.auth_service import AuthService


class LoginUseCase:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def execute(self, email: str, password: str) -> dict[str, str]:
        return self._auth_service.login(email=email, password=password)
