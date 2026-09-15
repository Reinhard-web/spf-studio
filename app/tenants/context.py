from typing import Annotated

from fastapi import Depends, Header, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.current_user import CurrentUser
from app.db.session import get_db
from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership

DbSession = Annotated[Session, Depends(get_db)]
OrganizationId = Annotated[int | None, Header(alias="X-Organization-ID")]


def get_current_membership(
    current_user: CurrentUser,
    db: DbSession,
    organization_id: OrganizationId,
) -> OrganizationMembership:
    if organization_id is None:
        raise HTTPException(
            status_code=400,
            detail="X-Organization-ID header is required",
        )

    membership = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == current_user.id,
            OrganizationMembership.organization_id == organization_id,
            OrganizationMembership.is_active.is_(True),
        )
    )

    if not membership:
        raise HTTPException(
            status_code=403,
            detail="User is not a member of this organization",
        )

    return membership


CurrentMembership = Annotated[
    OrganizationMembership,
    Depends(get_current_membership),
]


def get_current_organization(
    current_membership: CurrentMembership,
    db: DbSession,
) -> Organization:
    organization = db.scalar(
        select(Organization).where(
            Organization.id == current_membership.organization_id,
        )
    )

    if not organization:
        raise HTTPException(
            status_code=403,
            detail="Organization not found",
        )

    return organization


CurrentOrganization = Annotated[
    Organization,
    Depends(get_current_organization),
]