from math import perm
from app.models.permissions import Permissions
from sqlalchemy.orm import Session
from tests.utils.utils import random_lower_string
from app.crud.permission import permission
from app.core.enumarations import Permissions as PermissionsEnum

from app.schemas.permissions import PermissionCreate, PermissionUpdate, EndpointPermissions

def test_create_permissions(db: Session, user_id: int)-> None:
    permission_in = PermissionCreate(
        name=random_lower_string(),
        permissions={
            "event":PermissionsEnum.FULL,
            "user_events":PermissionsEnum.FULL
        }
    )
    new_permission = permission.create(db=db, obj_in=permission_in)

    assert new_permission.id is not None
    assert new_permission.name == permission_in.name
    assert new_permission.permissions == permission_in.permissions

def test_get_permissions(db: Session, user_id: int)-> None:
    permission_in = PermissionCreate(
        name=random_lower_string(),
        permissions={
            "event":PermissionsEnum.FULL,
            "user_events":PermissionsEnum.FULL
        }
    )
    new_permission = permission.create(db=db, obj_in=permission_in)

    my_permission = permission.get(db=db, id=new_permission.id)

    assert my_permission.id == new_permission.id
    assert my_permission.name == new_permission.name
    assert my_permission.permissions == new_permission.permissions

def test_update_permissions(db: Session, user_id: int)-> None:
    permission_in = PermissionCreate(
        name=random_lower_string(),
        permissions={
            "event":PermissionsEnum.FULL,
            "user_events":PermissionsEnum.FULL
        }
    )
    update_permission = PermissionUpdate(
        name=random_lower_string(),
        permissions={
            "event":PermissionsEnum.DENY,
            "user_events":PermissionsEnum.READ_ONLY
        }
    )
    new_permission = permission.create(db=db, obj_in=permission_in)

    updated_permission = permission.update(
        db=db,
        db_obj=new_permission,
        obj_in=update_permission
    )

    assert updated_permission.id == new_permission.id
    assert updated_permission.name == update_permission.name
    assert updated_permission.permissions == updated_permission.permissions

def test_delete_permissions(db: Session, user_id: int)-> None:
    permission_in = PermissionCreate(
        name=random_lower_string(),
        permissions={
            "event":PermissionsEnum.FULL,
            "user_events":PermissionsEnum.FULL
        }
    )
    new_permission = permission.create(db=db, obj_in=permission_in)
    permission.remove(db=db, id=new_permission.id)
    check_permission = permission.get(db=db, id=new_permission.id)


    assert new_permission.id is not None
    assert check_permission == None

    