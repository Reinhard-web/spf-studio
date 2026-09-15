from app.tenants.roles import OrganizationRole

ROLE_LEVELS: dict[OrganizationRole, int] = {
    OrganizationRole.MEMBER: 10,
    OrganizationRole.ADMIN: 20,
    OrganizationRole.OWNER: 30,
}


def has_role_level(
    role: str,
    required_role: OrganizationRole,
) -> bool:
    try:
        current_role = OrganizationRole(role)
    except ValueError:
        return False

    return ROLE_LEVELS[current_role] >= ROLE_LEVELS[required_role]