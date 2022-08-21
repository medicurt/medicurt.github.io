from fastapi import Depends, HTTPException, status
from typing import Any, List
from app.crud.user import user, user_subscription
from app.crud.event import crud_event
from app.crud.permission import permission
from app.schemas import User, UserCreate, UserUpdate
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user, ApiContext, get_api_context
from app.core.enumarations import Permissions
from app.schemas import UserSubscriptions
from app.schemas.user import UserSubscriptionCreate, UserSubscriptionsUpdate, UserSubscriptionsBase


router = APIRouter()

#Use this to create the first user. The author recommends using Postman API
@router.post(
    "/register-first-user", response_model=User, include_in_schema=True
)
def create_user_first(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
)-> Any:
    users = user.get_multi(db=db)
    if len(users) == 0:
        return user.create(db=db, obj_in=user_in)
    raise HTTPException(
        status_code=400,
        detail="First user already exists"
    )

@router.post(
    "/", response_model=User, include_in_schema=True
)
def create_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
)-> Any:
    existing = user.get_by_username(db=db, username=user_in.username)
    if existing is not None:
        raise HTTPException(
            status_code=400,
            detail="user already exists"
        )
    return user.create(db=db, obj_in=user_in)

@router.put(
    "/{id}", response_model=User, include_in_schema=True
)
def update_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
)-> Any:
    in_db = user.get(db=db, id=id)
    if in_db is not None:
        user.update(db=db, db_obj=in_db, obj_in=user_in)
    else:
        raise HTTPException(
            status_code=400,
            detail="user not found"
        )

@router.post(
    "/subscriptions", response_model=UserSubscriptions, include_in_schema=True
)
def create_subscription(
    *,
    db: Session = Depends(get_db),
    subscription_in = UserSubscriptionCreate,
    current_user: User = Depends(get_current_active_user)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="user_events",
        required_permission=Permissions.READ_WRITE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    return user_subscription.create(
        db=db,
        obj_in=subscription_in
    )

@router.get(
    "/subscriptions/{id}", response_model=UserSubscriptions, include_in_schema=True
)
def get_subscription(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    sub_id = id
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="user_events",
        required_permission=Permissions.READ_ONLY
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    return user_subscription.get(
        db=db,
        id=sub_id
    )


@router.get("/subscriptions", response_model=List[UserSubscriptions], include_in_schema=True)
def read(
    *,
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="user_events",
        required_permission=Permissions.READ_ONLY
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    return user_subscription.get_multi(
        db=db,
        skip=skip,
        limit=limit
    )

@router.put("/subscriptions/{id}", response_model=UserSubscriptions, include_in_schema=True)
def update(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    subscription_id = id,
    update_in = UserSubscriptionsUpdate
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="user_events",
        required_permission=Permissions.READ_WRITE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    in_db = user_subscription.get(
        db=db,
        id=subscription_id
    ) 
    if in_db != None:
        return user_subscription.update(
            db=db,
            db_obj=in_db,
            obj_in=UserSubscriptionsUpdate
        )
    else:
        raise HTTPException(status_code=400, detail="No subscription with the provided ID")

@router.delete("/subscriptions/{id}", response_model=UserSubscriptions, include_in_schema=True)
def remove(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    subscription_id: int,
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="user_events",
        required_permission=Permissions.FULL
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    in_db = user_subscription.get(
        db=db,
        id=subscription_id
    ) 
    if in_db != None:
        return user_subscription.remove(
            db=db,
            id=in_db.id
        )
    else:
        raise HTTPException(status_code=400, detail="No subscription with the provided ID")
        
