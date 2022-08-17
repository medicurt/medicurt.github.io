from math import perm
from app.models.permissions import Permissions
from sqlalchemy.orm import Session
from tests.utils.utils import random_lower_string
from app.crud.permission import permission

from app.schemas.permissions import PermissionCreate, PermissionUpdate, EndpointPermissions

def test_create_permissions(db: Session, user_id: int)-> None:
    permission_in = PermissionCreate(
        name=random_lower_string(),
        permissions={
            EndpointPermissions.event,
            EndpointPermissions.permissions,
        }
    )
    new_permission = permission.create(db=db, obj_in=permission_in)

    assert new_permission.id is not None
    assert new_permission.name == permission_in.name
    assert new_permission.permissions == permission_in.permissions
    