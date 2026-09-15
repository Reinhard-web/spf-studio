from sqlalchemy.orm import Session

from app.auth.passwords import hash_password
from app.models.organization import Organization
from app.models.organization_membership import OrganizationMembership
from app.models.user import User


def onboard_user(
    db: Session,
    email: str,
    full_name: str,
    password: str,
    organization_name: str,
    organization_slug: str,
) -> tuple[User, Organization]:
    user = User(
        email=email,
        full_name=full_name,
        password_hash=hash_password(password),
    )

    db.add(user)
    db.flush()

    organization = Organization(
        name=organization_name,
        slug=organization_slug,
    )

    db.add(organization)
    db.flush()

    membership = OrganizationMembership(
        user_id=user.id,
        organization_id=organization.id,
        role="owner",
    )

    db.add(membership)
    db.commit()

    db.refresh(user)
    db.refresh(organization)

    return user, organization