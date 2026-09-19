from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class CustomerValidation(Base):
    __tablename__ = "customer_validations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True,
    )

    experiment_id: Mapped[int | None] = mapped_column(
        ForeignKey("experiments.id"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    participant_type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    participant_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    method: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    objective: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    findings: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    customer_feedback: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    validation_result: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    validated_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )