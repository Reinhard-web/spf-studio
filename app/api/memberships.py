from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.auth.current_user import CurrentUser
from app.db.session import get_db
from app.schemas.membership import AddMemberRequest
from app.tenants.context import CurrentMembership
from app.tenants.memberships import add_member
from app.tenants.permissions import has_role_level
from app.tenants.roles import OrganizationRole

router = APIRouter(
    prefix="/memberships",
    tags=["Memberships"],
)

DbSession = Annotated[object, Depends(get_db)]


@router.post("")
def create_membership(
    request: AddMemberRequest,
    current_user: CurrentUser,
    current_membership: CurrentMembership,
    db: DbSession,
):
    if not has_role_level(
        current_membership.role,
        OrganizationRole.ADMIN,
    ):
        raise HTTPException(
            status_code=403,
            detail="Insufficient organization role",
        )

    try:
        membership = add_member(
            db,
            user_id=request.user_id,
            organization_id=current_membership.organization_id,
            role=request.role,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=400,
            detail=str(exc),
        ) from exc

    return {
        "id": membership.id,
        "user_id": membership.user_id,
        "organization_id": membership.organization_id,
        "role": membership.role,
        "is_active": membership.is_active,
    }