from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.passwords import verify_password
from app.auth.tokens import create_access_token
from app.models.user import User


def authenticate_user(
    db: Session,
    email: str,
    password: str,
) -> str | None:
    user = db.scalar(
        select(User).where(User.email == email)
    )

    if not user or not user.is_active:
        return None

    if not verify_password(password, user.password_hash):
        return None

    return create_access_token(str(user.id))