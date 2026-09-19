from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Idea(Base):
    __tablename__ = "ideas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    opportunity_id: Mapped[int | None] = mapped_column(
        ForeignKey("opportunities.id"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(200), nullable=False)

    description: Mapped[str] = mapped_column(Text, nullable=False)

    solution_concept: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    target_users: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    value_proposition: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    hypothesis: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    expected_outcome: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    success_conditions: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default="draft",
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