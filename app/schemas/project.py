from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProjectCreate(BaseModel):
    product_id: int
    name: str
    slug: str
    description: str | None = None
    project_type: str = "software"
    status: str = "planning"
    repository_url: str | None = None
    environment: str | None = None
    current_version: str | None = None


class ProjectUpdate(BaseModel):
    product_id: int | None = None
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    project_type: str | None = None
    status: str | None = None
    repository_url: str | None = None
    environment: str | None = None
    current_version: str | None = None


class ProjectResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    product_id: int
    name: str
    slug: str
    description: str | None
    project_type: str
    status: str
    repository_url: str | None
    environment: str | None
    current_version: str | None
    created_at: datetime
    updated_at: datetime