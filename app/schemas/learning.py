from datetime import datetime

from pydantic import BaseModel, ConfigDict


class LearningCreate(BaseModel):
    experiment_id: int | None = None
    title: str
    description: str
    learning_type: str
    confidence: str | None = None
    status: str = "active"


class LearningUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    learning_type: str | None = None
    confidence: str | None = None
    status: str | None = None


class LearningResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    experiment_id: int | None
    title: str
    description: str
    learning_type: str
    confidence: str | None
    status: str
    created_at: datetime
    updated_at: datetime