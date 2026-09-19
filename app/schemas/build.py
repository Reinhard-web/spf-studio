from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BuildCreate(BaseModel):
    project_id: int
    name: str
    version: str
    build_number: int | None = None
    status: str = "pending"
    environment: str = "development"
    branch: str | None = None
    commit_sha: str | None = None
    preview_url: str | None = None
    logs: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class BuildUpdate(BaseModel):
    project_id: int | None = None
    name: str | None = None
    version: str | None = None
    build_number: int | None = None
    status: str | None = None
    environment: str | None = None
    branch: str | None = None
    commit_sha: str | None = None
    preview_url: str | None = None
    logs: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class BuildResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    project_id: int
    name: str
    version: str
    build_number: int | None
    status: str
    environment: str
    branch: str | None
    commit_sha: str | None
    preview_url: str | None
    logs: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime