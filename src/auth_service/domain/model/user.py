# src/auth_service/domain/model/user.py
from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    id: str
    email: str
    hashed_password: str
    role: str
