# src/auth_service/application/logout_use_case.py
from ..domain.service.auth_service import AuthService


class LogoutUseCase:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def execute(self, refresh_token: str) -> None:
        self._auth_service.logout(refresh_token=refresh_token)
