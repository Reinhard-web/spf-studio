from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.organization import Organization  # noqa: E402, F401
from app.models.user import User  # noqa: E402, F401