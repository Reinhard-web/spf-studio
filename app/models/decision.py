from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Decision(Base):
    __tablename__ = "decisions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    problem_id: Mapped[int | None] = mapped_column(
        ForeignKey("problems.id"),
        nullable=True,
        index=True,
    )

    opportunity_id: Mapped[int | None] = mapped_column(
        ForeignKey("opportunities.id"),
        nullable=True,
        index=True,
    )

    idea_id: Mapped[int | None] = mapped_column(
        ForeignKey("ideas.id"),
        nullable=True,
        index=True,
    )

    experiment_id: Mapped[int | None] = mapped_column(
        ForeignKey("experiments.id"),
        nullable=True,
        index=True,
    )
    learning_id: Mapped[int | None] = mapped_column(
        ForeignKey("learnings.id"),
        nullable=True,
        index=True,
    )

    evidence_id: Mapped[int | None] = mapped_column(
        ForeignKey("evidence.id"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    decision: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    rationale: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="active",
    )

    decided_by: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    decided_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )