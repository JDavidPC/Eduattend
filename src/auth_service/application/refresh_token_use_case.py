# src/auth_service/application/refresh_token_use_case.py
from ..domain.service.auth_service import AuthService


class RefreshTokenUseCase:
    def __init__(self, auth_service: AuthService) -> None:
        self._auth_service = auth_service

    def execute(self, refresh_token: str) -> dict[str, str]:
        access_token = self._auth_service.refresh_access_token(refresh_token=refresh_token)
        return {"access_token": access_token}
