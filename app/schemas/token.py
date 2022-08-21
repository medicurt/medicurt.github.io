from typing import List
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    # permissions:

class TokenPayload(BaseModel):
    sub: int
    rid: int | None