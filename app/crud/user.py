from typing import Any, Dict, Optional, Union
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User, UserSubscriptions
from app.schemas.user import UserCreate, UserUpdate, UserSubscriptionCreate, UserSubscriptionsUpdate


#overrides the base methods for addtl functionality. This CRUD class is used for CRUDing users and requires
#extra functionality to support secure creation, access, and storage of user data. 

class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username = obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
            is_active = obj_in.is_active
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, username: str, password: str) -> Optional[User]:
        # verify username maps to a user
        user = self.get_by_username(db, username = username)
        if not user:
            return None
        # verify the password matches user password
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def is_active(self, user: User) -> bool:
        return user.is_active


user = CRUDUser(User)

class CRUDUserSubscriptions(CRUDBase[UserSubscriptions, UserSubscriptionCreate, UserSubscriptionsUpdate]):
    pass

user_subscription = CRUDUserSubscriptions(UserSubscriptions)
