from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProblemCreate(BaseModel):
    title: str
    description: str
    status: str = "new"
    domain: str | None = None
    source_type: str | None = None
    source_reference: str | None = None
    discovered_by: str | None = None
    urgency: str | None = None
    impact_potential: str | None = None
    strategic_relevance: str | None = None


class ProblemUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: str | None = None
    domain: str | None = None
    source_type: str | None = None
    source_reference: str | None = None
    discovered_by: str | None = None
    urgency: str | None = None
    impact_potential: str | None = None
    strategic_relevance: str | None = None


class ProblemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    title: str
    description: str
    status: str
    domain: str | None
    source_type: str | None
    source_reference: str | None
    discovered_by: str | None
    discovered_at: datetime
    urgency: str | None
    impact_potential: str | None
    strategic_relevance: str | None
    created_at: datetime
    updated_at: datetime