from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Experiment(Base):
    __tablename__ = "experiments"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    idea_id: Mapped[int] = mapped_column(
        ForeignKey("ideas.id"),
        nullable=False,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    objective: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    hypothesis: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    uncertainty: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    assumptions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    methodology: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    success_criteria: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    failure_criteria: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
    )

    outcome: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    results: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    learning: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )