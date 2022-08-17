import datetime
from app.crud.event import crud_event
from sqlalchemy.orm import Session
from app.schemas.event import EventCreate, EventUpdate, categoryEnum
from random import randint
from tests.utils.utils import random_lower_string, random_bool
from fastapi.encoders import jsonable_encoder
def create_random_event(db: Session, user_id: int)-> None:
    event_in = EventCreate(
        name=random_lower_string(),
        description=random_lower_string(),
        categories= [categoryEnum.ANIMALS, categoryEnum.ART, categoryEnum.MUSIC, categoryEnum.POLITICS],
        street_address=random_lower_string(),
        city=random_lower_string(),
        state_or_province=random_lower_string(),
        country=random_lower_string(),
        date_to_occur=jsonable_encoder(datetime.datetime.today()),
        recurring=random_bool(),
        admission_fee=randint(0,10000),
        is_open=random_bool(),
        max_participants=randint(1,100000),
        sort_order=randint(1,100000)
    )

    event = crud_event.create(
        db=db,
        obj_in=event_in
    )

    return event


def test_create_event(db: Session, user_id: int)-> None:
    event_in = EventCreate(
        name=random_lower_string(),
        description=random_lower_string(),
        categories= [categoryEnum.ANIMALS, categoryEnum.ART, categoryEnum.MUSIC, categoryEnum.POLITICS],
        street_address=random_lower_string(),
        city=random_lower_string(),
        state_or_province=random_lower_string(),
        country=random_lower_string(),
        date_to_occur=jsonable_encoder(datetime.datetime.today()),
        recurring=random_bool(),
        admission_fee=randint(0,10000),
        is_open=random_bool(),
        max_participants=randint(1,100000),
        sort_order=randint(1,100000)
    )

    event = crud_event.create(
        db=db,
        obj_in=event_in
    )

    assert event.id is not None
    assert event.admission_fee == event_in.admission_fee
    assert event.name == event_in.name
    assert event.description == event_in.description
    for i in event.categories:
        assert any(j == i for j in event_in.categories)
    assert event.street_address == event_in.street_address
    assert event.city == event_in.city
    assert event.state_or_province == event_in.state_or_province
    assert event.country == event_in.country
    assert event.date_to_occur == event_in.date_to_occur
    assert event.recurring == event_in.recurring
    assert event.admission_fee == event_in.admission_fee
    assert event.is_open == event_in.is_open    
    assert event.max_participants == event_in.max_participants
    assert event.sort_order == event_in.sort_order

def test_read_event(db: Session, user_id: int)-> None:
    event_in = EventCreate(
        name=random_lower_string(),
        description=random_lower_string(),
        categories= [categoryEnum.ANIMALS, categoryEnum.ART, categoryEnum.MUSIC, categoryEnum.POLITICS],
        street_address=random_lower_string(),
        city=random_lower_string(),
        state_or_province=random_lower_string(),
        country=random_lower_string(),
        date_to_occur=jsonable_encoder(datetime.datetime.today()),
        recurring=random_bool(),
        admission_fee=randint(0,10000),
        is_open=random_bool(),
        max_participants=randint(1,100000),
        sort_order=randint(1,100000)
    )

    entry = crud_event.create(
        db=db,
        obj_in=event_in
    )

    event = crud_event.get(
        db=db,
        id=entry.id
    )

    assert entry.id == event.id
    assert event.admission_fee == entry.admission_fee
    assert event.name == entry.name
    assert event.description == entry.description
    for i in event.categories:
        assert any(j == i for j in entry.categories)
    assert event.street_address == entry.street_address
    assert event.city == entry.city
    assert event.state_or_province == entry.state_or_province
    assert event.country == entry.country
    assert event.date_to_occur == entry.date_to_occur
    assert event.recurring == entry.recurring
    assert event.admission_fee == entry.admission_fee
    assert event.is_open == entry.is_open    
    assert event.max_participants == entry.max_participants
    assert event.sort_order == entry.sort_order
    

def test_update_event(db: Session, user_id: int) -> None:
    event = create_random_event(db=db, user_id=user_id)
    
    update_data = EventUpdate(
        name=random_lower_string(),
        description=random_lower_string(),
        street_address=random_lower_string(),
        country=random_lower_string(),
        state_or_province=random_lower_string(),
        recurring=not event.recurring,
        admission_fee=randint(0,100000),
        is_open=not event.is_open,
        max_participants=randint(0,100000),
        sort_order= randint(0,100000)
    )

    crud_event.update(
        db=db,
        db_obj=event,
        obj_in=update_data
    )

    assert event.name == update_data.name
    assert event.description == update_data.description
    assert event.street_address == update_data.street_address
    assert event.country == update_data.country
    assert event.state_or_province == update_data.state_or_province
    assert event.recurring == update_data.recurring
    assert event.admission_fee == update_data.admission_fee
    assert event.is_open == update_data.is_open
    assert event.max_participants == update_data.max_participants
    assert event.sort_order == update_data.sort_order


def test_delete_event(db: Session, user_id: int)-> None:
    event = create_random_event(db=db, user_id=user_id)
    deletion = crud_event.remove(db=db, id=event.id)
    confirmation = crud_event.get(db=db, id=event.id)

    assert event.id is not None
    assert confirmation is None