from datetime import datetime

from pydantic import BaseModel, ConfigDict


class OpportunityCreate(BaseModel):
    problem_id: int | None = None
    title: str
    description: str
    thesis: str | None = None
    target_users: str | None = None
    value_proposition: str | None = None
    potential_outcome: str | None = None
    technology_leverage: str | None = None
    strategic_relevance: str | None = None
    timing: str | None = None
    status: str = "discovered"


class OpportunityUpdate(BaseModel):
    problem_id: int | None = None
    title: str | None = None
    description: str | None = None
    thesis: str | None = None
    target_users: str | None = None
    value_proposition: str | None = None
    potential_outcome: str | None = None
    technology_leverage: str | None = None
    strategic_relevance: str | None = None
    timing: str | None = None
    status: str | None = None


class OpportunityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    problem_id: int | None
    title: str
    description: str
    thesis: str | None
    target_users: str | None
    value_proposition: str | None
    potential_outcome: str | None
    technology_leverage: str | None
    strategic_relevance: str | None
    timing: str | None
    status: str
    created_at: datetime
    updated_at: datetime