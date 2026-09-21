from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DeploymentCreate(BaseModel):
    build_id: int
    name: str
    version: str
    environment: str = "staging"
    target: str
    status: str = "pending"
    url: str | None = None
    logs: str | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class DeploymentUpdate(BaseModel):
    build_id: int | None = None
    name: str | None = None
    version: str | None = None
    environment: str | None = None
    target: str | None = None
    status: str | None = None
    url: str | None = None
    logs: str | None = None
    error_message: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class DeploymentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    build_id: int
    name: str
    version: str
    environment: str
    target: str
    status: str
    url: str | None
    logs: str | None
    error_message: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime