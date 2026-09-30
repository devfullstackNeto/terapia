import os
from datetime import datetime, timedelta, timezone

import jwt
from argon2 import PasswordHasher
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from sqlalchemy.orm import Session

from .db import get_db
from .models import User

ph = PasswordHasher()
oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/login")
SECRET = os.getenv("JWT_SECRET", "development-only-secret")
ALGORITHM = "HS256"


def hash_password(password: str) -> str:
    return ph.hash(password)


def verify_password(password: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, password)
    except Exception:
        return False


def create_token(user: User, minutes: int = 30) -> str:
    now = datetime.now(timezone.utc)
    payload = {
        "sub": str(user.id),
        "role": user.role,
        "iat": now,
        "exp": now + timedelta(minutes=minutes),
        "type": "access",
    }
    return jwt.encode(payload, SECRET, algorithm=ALGORITHM)


def current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        user = db.get(User, int(payload["sub"]))
    except (InvalidTokenError, KeyError, ValueError):
        user = None
    if not user or not user.active:
        raise HTTPException(401, "Credenciais inválidas", headers={"WWW-Authenticate": "Bearer"})
    return user


def require_roles(*roles: str):
    def dependency(user: User = Depends(current_user)) -> User:
        if user.role not in roles:
            raise HTTPException(403, "Acesso não autorizado para este perfil")
        return user

    return dependency
