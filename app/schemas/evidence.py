from datetime import datetime

from pydantic import BaseModel, ConfigDict


class EvidenceCreate(BaseModel):
    experiment_id: int | None = None
    title: str
    description: str
    evidence_type: str
    source_type: str | None = None
    source_reference: str | None = None
    status: str = "observed"
    observed_at: datetime | None = None


class EvidenceUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    evidence_type: str | None = None
    source_type: str | None = None
    source_reference: str | None = None
    status: str | None = None
    observed_at: datetime | None = None


class EvidenceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    experiment_id: int | None
    title: str
    description: str
    evidence_type: str
    source_type: str | None
    source_reference: str | None
    status: str
    observed_at: datetime | None
    created_at: datetime