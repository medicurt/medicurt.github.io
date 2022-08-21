import datetime
from typing import List
from pydantic import BaseModel, Field
from enum import Enum


#categoryEnum serves the purpose of offering strictly defined choices for the user and front-end dev
#for the purpose of sorting user inputs
class categoryEnum(str, Enum):
    ANIMALS = "Animals"
    OUTDOORS = "Outdoors"
    SPORTS = "Sports"
    TEAM_SPORTS = "Team Sports"
    VIDEO_GAMES = "Video Games"
    TABLETOP_GAMES = "Tabletop Games"
    MUSIC = "Music"
    ART = "Art"
    PROTEST = "Protest"
    POLITICS = "Politics"
    THEATRE = "Theatre"
    MARKET = "Market"
    CRAFTS = "Crafts"
    EDUCATION = "Education"
    HEALTH = "Health"
    FOOD = "Food"
    RELIGIOUS = "Religious"

# all fields in base are optional by default via the pipe operator
# since under most use cases, fields are generally not required, it's easier to start
# with default optional and explicit requirement
class EventBase(BaseModel):
    name: str | None = None
    description: str | None = None
    categories: List[categoryEnum] | None
    street_address: str | None = None
    city: str | None = None
    state_or_province: str | None = None
    country: str | None = None
    date_to_occur: datetime.datetime | None = None
    recurring: bool | None = None
    admission_fee: float | None = None
    is_open: bool | None = None
    max_participants: int | None = None
    sort_order: int | None = None


class EventCreate(EventBase):
    name: str = Field(..., min_length=1, max_length=300)
    description: str = Field(max_length=100000)
    street_address: str = Field(..., max_length=1000)
    city: str = Field(..., max_length=1000)
    state_or_province: str = Field(..., max_length=500)
    country: str = Field(..., max_length=500)
    date_to_occur: datetime.datetime = Field(...)
    # recurring left out, inheriting from base schema as optional is okay.

    # If no admission fee entered, schema defaults value to 0
    # ensures a non-negative value and allows only two decimal places
    admission_fee: int = Field(default=0, ge=0.0)
    is_open: bool = Field(default=True)
    # Inheriting max_participants from base schema is acceptable
    sort_order: int = Field(
        ...
    )


class EventUpdate(EventBase):
    # inheriting all other fields as optional from base is acceptable
    admission_fee: int = Field(ge=0.0)


class Event(EventBase):
    id: int | None
    created_by: int | None

    class Config:
        orm_mode = True
