from typing import Generator

from fastapi import Security, Depends, Header, Query, Cookie, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.api_key import APIKeyQuery, APIKeyCookie, APIKeyHeader, APIKey

from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, schemas
from app.models.user import User
from app.core import security
from app.core.config import settings
from app.db.session import SessionLocal

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_STR}/login")

API_KEY_NAME = "x-api-key"
HOST_KEY_NAME = "x-forwarded-host"


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)
api_key_cookie = APIKeyCookie(name=API_KEY_NAME, auto_error=False)

api_host_query = APIKeyQuery(name=HOST_KEY_NAME, auto_error=False)
api_host_header = APIKeyHeader(name=HOST_KEY_NAME, auto_error=False)
api_host_cookie = APIKeyCookie(name=HOST_KEY_NAME, auto_error=False)


async def get_api_key(
    api_key_query: str = Query(None, alias=API_KEY_NAME),
    api_key_header: str = Header(None, alias=API_KEY_NAME),
    api_key_cookie: str = Cookie(None, alias=API_KEY_NAME),
):
    if api_key_query is not None:
        return api_key_query
    elif api_key_header is not None:
        return api_key_header
    elif api_key_cookie is not None:
        return api_key_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


async def get_api_host(
    api_host_query: str = Query(None, alias=HOST_KEY_NAME),
    api_host_header: str = Header(None, alias=HOST_KEY_NAME),
    api_host_cookie: str = Cookie(None, alias=HOST_KEY_NAME),
):
    if api_host_query is not None:
        return api_host_query
    elif api_host_header is not None:
        return api_host_header
    elif api_host_cookie is not None:
        return api_host_cookie
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )


class ApiContext:
    def __init__(
        self,
        forwarded_host: str,
        forwarded_for: str = None,
        user_agent: str = None,
    ):
        self.forwarded_host = forwarded_host
        self.forwarded_for = forwarded_for
        self.user_agent = user_agent

    def get_domain_key(self):
        return self.forwarded_host


def get_api_context(
    x_api_key: str = Depends(get_api_key),
    x_forwarded_host: str = Depends(get_api_host),
    x_forwarded_for: str = Header(None),
    x_user_agent: str = Header(None),
):

    api_keys = [security.WEB_API_KEY, security.APP_API_KEY, security.PYTEST_API_KEY]
    if settings.LOCAL_API_KEY:
        api_keys.append(settings.LOCAL_API_KEY)

    if x_api_key in api_keys:
        return ApiContext(
            forwarded_host=x_forwarded_host,
            forwarded_for=x_forwarded_for,
            user_agent=x_user_agent,
        )
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authenticated"
        )


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not crud.user.is_active(current_user):
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def get_current_active_admin(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = crud.user.get(db, id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="User not found"
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    if not user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user doesn't have enough privileges",
        )
    return user
