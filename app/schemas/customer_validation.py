from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CustomerValidationCreate(BaseModel):
    experiment_id: int | None = None
    title: str
    participant_type: str | None = None
    participant_count: int | None = None
    method: str
    objective: str | None = None
    findings: str | None = None
    customer_feedback: str | None = None
    validation_result: str
    notes: str | None = None
    validated_at: datetime | None = None


class CustomerValidationUpdate(BaseModel):
    title: str | None = None
    participant_type: str | None = None
    participant_count: int | None = None
    method: str | None = None
    objective: str | None = None
    findings: str | None = None
    customer_feedback: str | None = None
    validation_result: str | None = None
    notes: str | None = None
    validated_at: datetime | None = None


class CustomerValidationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    experiment_id: int | None
    title: str
    participant_type: str | None
    participant_count: int | None
    method: str
    objective: str | None
    findings: str | None
    customer_feedback: str | None
    validation_result: str
    notes: str | None
    validated_at: datetime | None
    created_at: datetime