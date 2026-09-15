from datetime import UTC, datetime, timedelta

import jwt

from app.core.config import settings


def create_access_token(subject: str) -> str:
    expires_at = datetime.now(UTC) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )

    payload = {
        "sub": subject,
        "exp": expires_at,
    }

    return jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm,
    )


def decode_access_token(token: str) -> str:
    payload = jwt.decode(
        token,
        settings.jwt_secret_key,
        algorithms=[settings.jwt_algorithm],
    )

    subject = payload.get("sub")

    if not subject:
        raise ValueError("Token subject is missing")

    return subject