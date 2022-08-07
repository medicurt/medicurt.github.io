from pydantic import Field
from pydantic import BaseModel
from app.core.enumarations import Permissions

# This schema automatically defaults all user permissions to DENY, and these can later be set to different permission values
# by accessing the permissions endpoint.
class EndpointPermissions(BaseModel):
    event: Permissions = Permissions.DENY
    permissions: Permissions = Permissions.DENY


# At base, all fields are optional (thus '| None') and will be switched to required as needed by inheriting schemas
class PermissionBase(BaseModel):
    name: str | None = Field(None)
    description: str | None = Field(None)
    permissions: EndpointPermissions | None = Field(None)


class PermissionCreate(PermissionBase):
    name: str = Field(
        ...  # elipses means 'required', schema will reject incoming data missing these fields
    )
    permissions: EndpointPermissions = Field(...)


class PermissionUpdate(PermissionBase):
    pass  # directly inherits PermissionBase and makes no changes


class Permission(PermissionBase):
    id: int | None
