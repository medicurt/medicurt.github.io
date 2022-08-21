from datetime import datetime
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from app.core.config import settings
from tests.utils.utils import random_bool, random_lower_string
from random import randint
from fastapi.encoders import jsonable_encoder

def test_post_login(
    client: TestClient, user_headers: dict, db: Session
)-> None:


    response = client.post(
        f"{settings.API_STR}/login/",
        headers=user_headers,
    )

    assert response.status_code == 200
    content = response.json()

    assert "id" in content