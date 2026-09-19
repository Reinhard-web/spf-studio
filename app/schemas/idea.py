from datetime import datetime

from pydantic import BaseModel, ConfigDict


class IdeaCreate(BaseModel):
    opportunity_id: int | None = None
    title: str
    description: str
    solution_concept: str | None = None
    target_users: str | None = None
    value_proposition: str | None = None
    hypothesis: str | None = None
    expected_outcome: str | None = None
    success_conditions: str | None = None
    status: str = "draft"


class IdeaUpdate(BaseModel):
    opportunity_id: int | None = None
    title: str | None = None
    description: str | None = None
    solution_concept: str | None = None
    target_users: str | None = None
    value_proposition: str | None = None
    hypothesis: str | None = None
    expected_outcome: str | None = None
    success_conditions: str | None = None
    status: str | None = None


class IdeaResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    opportunity_id: int | None
    title: str
    description: str
    solution_concept: str | None
    target_users: str | None
    value_proposition: str | None
    hypothesis: str | None
    expected_outcome: str | None
    success_conditions: str | None
    status: str
    created_at: datetime
    updated_at: datetime