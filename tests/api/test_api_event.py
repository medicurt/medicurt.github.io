from datetime import datetime
import json
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from tests.utils.utils import random_bool, random_lower_string
from random import randint
from fastapi.encoders import jsonable_encoder
from app.schemas.event import EventCreate
from app.crud.event import crud_event
from random import randint


def test_post_event(
    client: TestClient, user_headers: dict, db: Session
)-> None:
    data = {
        'name':random_lower_string(),
        'description':random_lower_string(),
        'street_address':random_lower_string(),
        'city':random_lower_string(),
        'state_or_province':random_lower_string(),
        'country':random_lower_string(),
        'date_to_occur':jsonable_encoder(datetime.today()),
        'admission_fee':randint(1,100),
        'is_open':random_bool(),
        'sort_order':randint(100,1000)
    }

    response = client.post(
        f"{settings.API_STR}/event/",
        headers=user_headers,
        json=data
    )

    assert response.status_code == 200
    content = response.json()

    assert "id" in content


def test_get_event(
    client: TestClient, user_headers: dict, db: Session
)-> None:
    event_in=EventCreate(
            name=random_lower_string(),
            description=random_lower_string(),
            street_address=random_lower_string(),
            city=random_lower_string(),
            state_or_province=random_lower_string(),
            country=random_lower_string(),
            date_to_occur=datetime.now(),
            admission_fee=randint(1,1000),
            is_open= True,
            sort_order=randint(1,1000)
        )
    event_in_dict = dict(event_in)
    my_event = crud_event.create(
        db=db,
        obj_in=event_in
    )

    response = client.get(
        f"{settings.API_STR}/event/{my_event.id}",
        headers=user_headers,
    )

    assert response.status_code == 200
    content = response.json()

    assert "id" in content
    for key in event_in_dict:
        if key == "date_to_occur":
            assert jsonable_encoder(content[key]) == jsonable_encoder(event_in_dict[key])
        else:
            assert event_in_dict[key] == content[key]


def test_get_multi_events(
    client: TestClient, user_headers: dict, db: Session
)-> None:
    event_in=EventCreate(
            name=random_lower_string(),
            description=random_lower_string(),
            street_address=random_lower_string(),
            city=random_lower_string(),
            state_or_province=random_lower_string(),
            country=random_lower_string(),
            date_to_occur=datetime.now(),
            admission_fee=randint(1,1000),
            is_open= True,
            sort_order=randint(1,1000)
        )
    event_in_dict = dict(event_in)
    my_event = crud_event.create(
        db=db,
        obj_in=event_in
    )

    response = client.get(
        f"{settings.API_STR}/event/",
        headers=user_headers,
    )

    assert response.status_code == 200
    content = response.json()
    assert any(i["id"] == my_event.id for i in content)


def test_update_event(
    client: TestClient, user_headers: dict, db: Session
)-> None:
    event_in=EventCreate(
            name=random_lower_string(),
            description=random_lower_string(),
            street_address=random_lower_string(),
            city=random_lower_string(),
            state_or_province=random_lower_string(),
            country=random_lower_string(),
            date_to_occur=datetime.now(),
            admission_fee=randint(1,100),
            is_open= True,
            sort_order=randint(1,100)
        )
    update_event = EventCreate(
            name=random_lower_string(),
            description=random_lower_string(),
            street_address=random_lower_string(),
            city=random_lower_string(),
            state_or_province=random_lower_string(),
            country=random_lower_string(),
            date_to_occur=datetime.now(),
            admission_fee=randint(101,200),
            is_open= False,
            sort_order=randint(101,200)
        )
    update_event_dict = dict(update_event)
    data = jsonable_encoder(update_event)

    my_event = crud_event.create(
        db=db,
        obj_in=event_in
    )

    response = client.put(
        f"{settings.API_STR}/event/{my_event.id}",
        headers=user_headers,
        json=data
    )

    assert response.status_code == 200
    content = response.json()
    for key in update_event_dict:
        if key == "date_to_occur":
            assert jsonable_encoder(content[key]) == jsonable_encoder(update_event_dict[key])
        else:
            assert update_event_dict[key] == content[key]


def test_delete_event(
    client: TestClient, user_headers: dict, db: Session
)-> None:
    event_in=EventCreate(
            name=random_lower_string(),
            description=random_lower_string(),
            street_address=random_lower_string(),
            city=random_lower_string(),
            state_or_province=random_lower_string(),
            country=random_lower_string(),
            date_to_occur=datetime.now(),
            admission_fee=randint(1,100),
            is_open= True,
            sort_order=randint(1,100)
        )
    my_event = crud_event.create(
        db=db, obj_in=event_in
    )

    response = client.delete(
        f"{settings.API_STR}/event/{my_event.id}",
        headers=user_headers
    )

    check_event = crud_event.get(
        db=db, id=my_event.id
    )

    assert check_event is None
