from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ExperimentCreate(BaseModel):
    idea_id: int
    title: str
    objective: str
    hypothesis: str
    uncertainty: str | None = None
    assumptions: str | None = None
    methodology: str
    success_criteria: str
    failure_criteria: str | None = None
    status: str = "draft"


class ExperimentUpdate(BaseModel):
    title: str | None = None
    objective: str | None = None
    hypothesis: str | None = None
    uncertainty: str | None = None
    assumptions: str | None = None
    methodology: str | None = None
    success_criteria: str | None = None
    failure_criteria: str | None = None
    status: str | None = None
    outcome: str | None = None
    results: str | None = None
    learning: str | None = None


class ExperimentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    idea_id: int
    title: str
    objective: str
    hypothesis: str
    uncertainty: str | None
    assumptions: str | None
    methodology: str
    success_criteria: str
    failure_criteria: str | None
    status: str
    outcome: str | None
    results: str | None
    learning: str | None
    created_at: datetime
    updated_at: datetime