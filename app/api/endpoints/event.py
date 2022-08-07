from fastapi import Depends, HTTPException, status
from typing import Any, List
from app.crud.event import crud_event
from app.crud.permission import permission
from app.schemas import Event, EventCreate, EventUpdate
from app.schemas import User
from fastapi.routing import APIRouter
from sqlalchemy.orm import Session
from app.core.dependencies import get_db, get_current_active_user, ApiContext, get_api_context
from app.core.enumarations import Permissions

router = APIRouter()
#this endpoint allows authorized users to create, read, update, and delete events

#gets a list of available events
@router.get("/", response_model=List[Event], include_in_schema=True)
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
        permission="event",
        required_permission=Permissions.READ_ONLY
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    return crud_event.get_multi(
        db=db,
        skip=skip,
        limit=limit
    )

#creates an event, returning Event data in an Event schema
@router.post("/", response_model=Event, include_in_schema=True)
def create(
    *,
    db: Session = Depends(get_db),
    item_in: EventCreate,
    current_user: User = Depends(get_current_active_user),
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="event",
        required_permission=Permissions.READ_WRITE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    return crud_event.create(
        db=db,
        obj_in=item_in
    )

#takes an id as a path parameter, which is then used to find and update an item in db
@router.put("/{id}", response_model=Event, include_in_schema=True)
def update(
    *,
    db: Session = Depends(get_db),
    id: int,
    event_in: EventUpdate,
    current_user: User = Depends(get_current_active_user),
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="event",
        required_permission=Permissions.READ_WRITE
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    event = crud_event.get(
        db=db,
        id=id
    )
    return crud_event.update(
        db=db,
        db_obj=event,
        obj_in=event_in
    )

#takes an id as a path parameter, which is then used to find an item in db
@router.get("/{id}", response_model=Event, include_in_schema=True)
def read(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user)
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="event",
        required_permission=Permissions.READ_ONLY
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    event = crud_event.get(
        db=db,
        id=id,
    )
    if not event:
        raise HTTPException(status_code=404, detail="Whoops, we couldn't find that!")
    return event

#takes id as a path parameter to find and delete an object in a db.
@router.delete("/{id}", response_model=Event)
def remove_item(
    *,
    db: Session = Depends(get_db),
    id: int,
    current_user: User = Depends(get_current_active_user)
)-> Any:
    if not permission.has_permission(
        db=db,
        user_id=current_user.id,
        permission_id=current_user.permissions_id,
        permission="event",
        required_permission=Permissions.FULL
    ):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Unauthorized!"
        )
    event = crud_event.get(
        db=db,
        id=id
    )
    if not event:
        raise HTTPException(status_code=404, detail="Whoops, we couldn't find that!")
    return crud_event.remove(
        db=db,
        id=id
    )