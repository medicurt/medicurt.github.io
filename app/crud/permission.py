from typing import Any, List
from app.crud.base import CRUDBase
from app.crud import user
from app.models import User as user_model
from app.crud import permission as crud_permission
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
        user_seeking_permissions = db.query(user_model).filter_by(id = user_id).first()
        user_permissions = self.get(
            db=db, id=user_seeking_permissions.permissions_id
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
            elif access_level == "FULL":
                return True
        return False

permission = CRUDPermissions(PermissionModel)