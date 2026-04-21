# src/auth_service/domain/service/auth_service.py
from datetime import UTC, datetime, timedelta
from typing import Protocol

import bcrypt
import jwt

from ..exception.auth_exceptions import InvalidCredentialsError, TokenExpiredError
from ..model.user import User


class IUserRepository(Protocol):
    def find_by_email(self, email: str) -> User | None: ...


class ITokenStore(Protocol):
    def save(self, token: str, user_id: str) -> None: ...

    def exists(self, token: str) -> bool: ...

    def delete(self, token: str) -> None: ...


class AuthService:
    def __init__(
        self,
        repository: IUserRepository,
        token_store: ITokenStore,
        jwt_secret: str,
        access_token_minutes: int = 30,
        refresh_token_days: int = 7,
    ) -> None:
        self._repository = repository
        self._token_store = token_store
        self._jwt_secret = jwt_secret
        self._access_token_minutes = access_token_minutes
        self._refresh_token_days = refresh_token_days

    def login(self, email: str, password: str) -> dict[str, str]:
        user = self._repository.find_by_email(email)
        if user is None:
            raise InvalidCredentialsError("Credenciales invalidas.")

        if not bcrypt.checkpw(password.encode("utf-8"), user.hashed_password.encode("utf-8")):
            raise InvalidCredentialsError("Credenciales invalidas.")

        access_token = self._encode_access_token(user)
        refresh_token = self._encode_refresh_token(user)
        self._token_store.save(refresh_token, user.id)

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def refresh_access_token(self, refresh_token: str) -> str:
        payload = self._decode_refresh_token(refresh_token)
        user = User(
            id=str(payload["sub"]),
            email=str(payload["email"]),
            hashed_password="",
            role=str(payload["role"]),
        )
        return self._encode_access_token(user)

    def logout(self, refresh_token: str) -> None:
        self._token_store.delete(refresh_token)

    def _encode_access_token(self, user: User) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "token_type": "access",
            "iat": now,
            "exp": now + timedelta(minutes=self._access_token_minutes),
        }
        return str(jwt.encode(payload, self._jwt_secret, algorithm="HS256"))

    def _encode_refresh_token(self, user: User) -> str:
        now = datetime.now(UTC)
        payload = {
            "sub": user.id,
            "email": user.email,
            "role": user.role,
            "token_type": "refresh",
            "iat": now,
            "exp": now + timedelta(days=self._refresh_token_days),
        }
        return str(jwt.encode(payload, self._jwt_secret, algorithm="HS256"))

    def _decode_refresh_token(self, refresh_token: str) -> dict:
        if not self._token_store.exists(refresh_token):
            raise InvalidCredentialsError("Refresh token no valido.")

        try:
            payload = jwt.decode(refresh_token, self._jwt_secret, algorithms=["HS256"])
        except jwt.ExpiredSignatureError as exc:
            self._token_store.delete(refresh_token)
            raise TokenExpiredError("El refresh token ha expirado.") from exc
        except jwt.InvalidTokenError as exc:
            raise InvalidCredentialsError("Refresh token no valido.") from exc

        if payload.get("token_type") != "refresh":
            raise InvalidCredentialsError("Refresh token no valido.")

        return payload
