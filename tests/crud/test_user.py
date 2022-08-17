import datetime
from app.crud.user import user
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, User, UserSubscriptionCreate, UserSubscriptionsUpdate
from random import randint
from tests.utils.utils import random_lower_string, random_bool
from fastapi.encoders import jsonable_encoder
from app.crud.user import user_subscription
from tests.crud.test_event import create_random_event

#Use this method with hard-coded values to implement first user data
def test_create_user(db: Session, user_id: int)-> None:
    user_in = UserCreate(
        username="user@example.com",
        is_superuser=True,
        is_active=True,
        permissions_id=None,
        events_owned=None,
        events_subscribed=None,
        password="mypassword"
    )

    new_user = user.create(
        db=db,
        obj_in=user_in
    )

    assert new_user.id is not None
    assert new_user.id == 0


def test_create_subscription(db: Session, user_id: int)-> None:
    event = create_random_event(db=db, user_id=user_id)
    sub_in = UserSubscriptionCreate(
        user_id=user_id,
        event_id=event.id
    )
    subscription = user_subscription.create(
        db=db,
        obj_in=sub_in
    )

    assert subscription.id is not None
    assert subscription.user_id == user_id
    assert subscription.event_id == event.id

def test_read_subscription(db: Session, user_id: int)-> None:
    event = create_random_event(db=db, user_id=user_id)
    sub_in = UserSubscriptionCreate(
        user_id=user_id,
        event_id=event.id
    )
    sub = user_subscription.create(
        db=db,
        obj_in=sub_in
    )
    subscription = user_subscription.get(
        db=db,
        id=sub.id
    )
    assert id is not None
    assert subscription.event_id == event.id
    assert subscription.user_id == user_id

def test_update_subscription(db: Session, user_id: int)-> None:
    event = create_random_event(db=db, user_id=user_id)
    sub_in = UserSubscriptionCreate(
        user_id=user_id,
        event_id=event.id
    )
    sub = user_subscription.create(
        db=db,
        obj_in=sub_in
    )
    sub_in = UserSubscriptionCreate(
        user_id=user_id,
        event_id=event.id
    )
    sub_2 = user_subscription.create(
        db=db,
        obj_in=sub_in
    )
    #Sub_in is re-written here
    sub_in = UserSubscriptionsUpdate(
        event_id=sub_2.event_id
    )
    subscription = user_subscription.update(
        db=db,
        db_obj=sub,
        obj_in=sub_in
    )
    assert subscription.event_id == sub_2.event_id

def test_delete_subscription(db: Session, user_id: int)-> None:
    event = create_random_event(db=db, user_id=user_id)
    sub_in = UserSubscriptionCreate(
        user_id=user_id,
        event_id=event.id
    )
    sub = user_subscription.create(
        db=db,
        obj_in=sub_in
    )
    deleted_sub = user_subscription.remove(
        db=db,
        id=sub.id
    )
    confirmation = user_subscription.get(
        db=db,
        id=sub.id
    )
    assert confirmation is None
