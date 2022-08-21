from typing import Any
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app import crud, schemas
from app.core.security import create_access_token
from app.schemas.token import LoginResponse
from app.core import dependencies
from app.core.config import settings
from app.core.security import (
    get_password_hash,
)

router = APIRouter()

# Returns an OAuth2 token in order to validate user access for a period of time

@router.post("/login/", response_model=schemas.LoginResponse)
def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
    api_context: dependencies.ApiContext = Depends(dependencies.get_api_context)
) -> Any:
    user = crud.user.authenticate(
        db=db, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password or both"
        )
    token = create_access_token(
        user_id=user.id
    )
    return {
        "access_token": token,
        "token_type":"bearer",
    }