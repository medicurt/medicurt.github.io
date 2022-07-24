from pydantic import BaseModel, Field

#base class is always optional, as fields are only required under specific circumstances
class UserBase(BaseModel):
    username: str | None = None
    is_superuser: bool = Field(default = False)
    is_active: bool | None = True

#password can be any length greater than ten up to 1000 characters (to prevent db overflow attacks)
class UserCreate(UserBase):
    username: str = Field(
        ..., min_length = 1, max_length = 32
    )
    password: str = Field(
        ..., min_length=10, max_length=1000
    )

class UserUpdate(UserBase):
    password: str | None = None

class User(UserBase):
    id: int | None

    class Config:
        orm_mode = True

class UserInDB(User):
    hashed_password: str


