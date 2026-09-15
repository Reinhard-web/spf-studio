from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
from app.models.user import User


def create_organization(
    db: Session,
    name: str,
    slug: str,
    owner: User,
) -> Organization:
    organization = Organization(
        name=name,
        slug=slug,
    )

    db.add(organization)
    db.flush()

    membership = OrganizationMembership(
        user_id=owner.id,
        organization_id=organization.id,
        role="owner",
    )

    db.add(membership)
    db.commit()
    db.refresh(organization)

    return organization