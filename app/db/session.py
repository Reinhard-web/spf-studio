from collections.abc import Generator

from sqlalchemy.orm import Session, sessionmaker

from app.db.database import engine

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()