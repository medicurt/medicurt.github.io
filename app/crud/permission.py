from typing import Any, List
from app.crud.base import CRUDBase
from app.core.enumarations import Permissions
from app.models.permissions import Permissions as PermissionModel
from app.schemas.permissions import PermissionCreate, PermissionUpdate
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

class CRUDPermissions(CRUDBase[PermissionModel, PermissionCreate, PermissionUpdate]):
    def get_field_options(
        self, db: Session, *, user_id: int
    )-> List[Any]:
        options = (
            db.query(
                self.model.id.label("code"),
                self.model.name.label("value"),
            )
            .order_by(self.model.name)
            .all()
        )
        result = []
        for row in options:
            result.append(
                {
                    "code": str(row.code),
                    "value": row.value,
                }
            )
        return result

    def has_permission(
        self,
        db: Session,
        *,
        user_id: int,
        permission_id: int,
        permission: str,
        required_permission: Permissions
    ) -> bool:
        #Admins and superusers have permission ID 0.
        if permission_id == 0:
            return True
        user_permissions = self.get(
            db=db,
            user_id=user_id,
            id=permission_id
        )
        authorization = user_permissions.permissions
        if permission in authorization:
            access_level = authorization[permission]
            if access_level == Permissions.DENY:
                return False
            elif required_permission == Permissions.READ_ONLY and access_level == "R":
                return True
            elif required_permission == Permissions.READ_WRITE and access_level in ["R", "RW"]:
                return True
            elif required_permission == Permissions.FULL and access_level == "FULL":
                return True
        return False

permission = CRUDPermissions(PermissionModel)