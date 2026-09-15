from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.organization_membership import OrganizationMembership
from app.models.user import User
from app.tenants.roles import OrganizationRole


def add_member(
    db: Session,
    user_id: int,
    organization_id: int,
    role: OrganizationRole = OrganizationRole.MEMBER,
) -> OrganizationMembership:
    user = db.scalar(
        select(User).where(User.id == user_id)
    )

    if not user:
        raise ValueError("User not found")

    membership = db.scalar(
        select(OrganizationMembership).where(
            OrganizationMembership.user_id == user_id,
            OrganizationMembership.organization_id == organization_id,
        )
    )

    if membership:
        raise ValueError("User is already a member of this organization")

    membership = OrganizationMembership(
        user_id=user_id,
        organization_id=organization_id,
        role=role.value,
    )

    db.add(membership)
    db.commit()
    db.refresh(membership)

    return membership