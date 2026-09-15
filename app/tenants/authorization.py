from typing import Annotated

from fastapi import Depends, HTTPException

from app.tenants.context import CurrentMembership
from app.tenants.permissions import has_role_level
from app.tenants.roles import OrganizationRole


def require_role(required_role: OrganizationRole):
    def dependency(
        membership: CurrentMembership,
    ) -> None:
        if not has_role_level(membership.role, required_role):
            raise HTTPException(
                status_code=403,
                detail="Insufficient organization role",
            )

    return dependency


def require_owner() -> None:
    return require_role(OrganizationRole.OWNER)


def require_admin() -> None:
    return require_role(OrganizationRole.ADMIN)


def require_member() -> None:
    return require_role(OrganizationRole.MEMBER)


OwnerRequired = Annotated[
    None,
    Depends(require_owner()),
]

AdminRequired = Annotated[
    None,
    Depends(require_admin()),
]

MemberRequired = Annotated[
    None,
    Depends(require_member()),
]