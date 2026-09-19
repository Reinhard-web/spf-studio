from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DecisionCreate(BaseModel):
    problem_id: int | None = None
    opportunity_id: int | None = None
    idea_id: int | None = None
    experiment_id: int | None = None
    learning_id: int | None = None
    evidence_id: int | None = None
    title: str
    decision: str
    rationale: str | None = None
    status: str = "active"
    decided_by: str | None = None


class DecisionUpdate(BaseModel):
    title: str | None = None
    decision: str | None = None
    rationale: str | None = None
    status: str | None = None
    decided_by: str | None = None
    learning_id: int | None = None
    evidence_id: int | None = None


class DecisionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    problem_id: int | None
    opportunity_id: int | None
    idea_id: int | None
    experiment_id: int | None
    learning_id: int | None
    evidence_id: int | None
    title: str
    decision: str
    rationale: str | None
    status: str
    decided_by: str | None
    decided_at: datetime
    created_at: datetime