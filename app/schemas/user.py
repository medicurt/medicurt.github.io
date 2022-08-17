from pydantic import BaseModel, Field
from app.schemas.event import Event
from typing import List

# base class is always optional, as fields are only required under specific circumstances
class UserBase(BaseModel):
    username: str | None = None
    is_superuser: bool = Field(default=False)
    is_active: bool | None = True
    permissions_id: int | None = None


# password can be any length greater than ten up to 1000 characters (to prevent db overflow attacks)
class UserCreate(UserBase):
    username: str = Field(..., min_length=1, max_length=32)
    password: str = Field(..., min_length=10, max_length=1000)


class UserUpdate(UserBase):
    password: str | None = None


class User(UserBase):
    id: int | None

    class Config:
        orm_mode = True


class UserInDB(User):
    hashed_password: str


class UserSubscriptionsBase(BaseModel):
    user_id: int | None
    event_id: int | None

class UserSubscriptionCreate(UserSubscriptionsBase):
    user_id: int = Field(
        ...
    )
    event_id: int = Field(
        ...
    )

class UserSubscriptionsUpdate(UserSubscriptionsBase):
    pass

class UserSubscriptions(UserSubscriptionsBase):
    id: int | None
