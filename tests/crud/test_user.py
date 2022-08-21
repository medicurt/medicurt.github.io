import datetime
from app.crud.user import user
from sqlalchemy.orm import Session
from app.schemas.user import UserCreate, UserUpdate, User, UserSubscriptionCreate, UserSubscriptionsUpdate
from random import randint
from tests.utils.utils import random_lower_string, random_bool
from fastapi.encoders import jsonable_encoder
from app.crud.user import user_subscription
from tests.crud.test_event import create_random_event
from app.core.config import settings
from app.core.security import create_access_token

def test_create_jwt()-> None:
    a_token = {"token":create_access_token(user_id=1), "type":"bearer"}
    assert a_token["token"] != None

def test_authentication(db: Session, user_id: int)-> None:
    curr_user = user.authenticate(db=db, username=settings.PYTEST_USER, password=settings.PYTEST_PASSWORD)
    assert curr_user != None

# def test_get_by_username(db: Session)-> None:
#     curr_user = user.get_by_username(db=db, username=settings.PYTEST_USER)
#     assert curr_user != None

# Use this method with hard-coded values to implement first user data
#THE PASSWORD STRING MUST BE HARDCODED, THE DB STORES HASHED PASSWORDS ONLY
#YOU WILL NOT BE ABLE TO RECOVER THE PASSWORD IF LOST
# Set superuser to True while creating your account
# Consider disabling all asserts except that id is not none to avoid throwing a test failure
#
def test_create_user(db: Session, user_id: int)-> None:
    user_in = UserCreate(
        username=random_lower_string(10)+"@example.com",
        is_superuser=False,
        is_active=True,
        permissions_id=None,
        events_owned=None,
        events_subscribed=None,
        password=random_lower_string()
    )

    new_user = user.create(
        db=db,
        obj_in=user_in
    )

    assert new_user.id is not None
    assert new_user.username == user_in.username
    assert new_user.hashed_password != user_in.password
    assert user.authenticate(db=db, username=new_user.username, password=user_in.password) != None


def test_get_user(db: Session, user_id: int)-> None:
    user_in = UserCreate(
        username=random_lower_string(10)+"@example.com",
        is_superuser=False,
        is_active=True,
        permissions_id=None,
        events_owned=None,
        events_subscribed=None,
        password=random_lower_string()
    )

    new_user = user.create(
        db=db,
        obj_in=user_in
    )

    my_user = user.get(
        db=db,
        id=new_user.id
    )

    assert my_user.id == new_user.id
    assert my_user.username == new_user.username

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
