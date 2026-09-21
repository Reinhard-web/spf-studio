from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TestCreate(BaseModel):
    build_id: int
    name: str
    test_type: str = "automated"
    status: str = "pending"
    environment: str = "development"
    command: str | None = None
    results: str | None = None
    logs: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class TestUpdate(BaseModel):
    build_id: int | None = None
    name: str | None = None
    test_type: str | None = None
    status: str | None = None
    environment: str | None = None
    command: str | None = None
    results: str | None = None
    logs: str | None = None
    started_at: datetime | None = None
    completed_at: datetime | None = None


class TestResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    build_id: int
    name: str
    test_type: str
    status: str
    environment: str
    command: str | None
    results: str | None
    logs: str | None
    started_at: datetime | None
    completed_at: datetime | None
    created_at: datetime
    updated_at: datetime