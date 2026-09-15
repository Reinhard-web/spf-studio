from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.auth.current_user import CurrentUser
from app.db.session import get_db
from app.tenants.organizations import get_user_organizations

router = APIRouter(
    prefix="/organizations",
    tags=["Organizations"],
)

DbSession = Annotated[Session, Depends(get_db)]


@router.get("")
def list_organizations(
    current_user: CurrentUser,
    db: DbSession,
):
    organizations = get_user_organizations(
        db,
        current_user.id,
    )

    return [
        {
            "id": organization.id,
            "name": organization.name,
            "slug": organization.slug,
        }
        for organization in organizations
    ]