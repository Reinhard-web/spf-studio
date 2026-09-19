from pydantic import BaseModel

from app.tenants.roles import OrganizationRole


class AddMemberRequest(BaseModel):
    user_id: int
    role: OrganizationRole = OrganizationRole.MEMBER