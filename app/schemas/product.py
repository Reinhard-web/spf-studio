from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ProductCreate(BaseModel):
    name: str
    slug: str
    description: str | None = None
    product_type: str = "software"
    studio: str | None = None
    status: str = "idea"
    idea_id: int | None = None


class ProductUpdate(BaseModel):
    name: str | None = None
    slug: str | None = None
    description: str | None = None
    product_type: str | None = None
    studio: str | None = None
    status: str | None = None
    idea_id: int | None = None


class ProductResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    organization_id: int
    idea_id: int | None
    name: str
    slug: str
    description: str | None
    product_type: str
    studio: str | None
    status: str
    created_at: datetime
    updated_at: datetime