import random
import string
from fastapi.testclient import TestClient
from typing import Dict
from app.core.config import settings
from json import dumps

def random_lower_string(length: int = 40) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))

def random_bool():
    my_bool = random.randint(0,1)
    if my_bool:
        return True
    return False

def get_user_headers(client: TestClient) -> Dict[str, str]:
    login_data = {
        "username": settings.PYTEST_USER,
        "password": settings.PYTEST_PASSWORD
    }
    login_headers = {
        "x-api-key": settings.SECRET_KEY
    }
    r = client.post(
        f"{settings.API_STR}/login/", data=login_data, headers=login_headers
    )
    tokens = r.json()
    if len(tokens) < 2:
        raise ValueError(tokens)
    a_token = tokens["access_token"]
    headers = {
        "Authorization": f"Bearer {a_token}",
        "x-api-key": settings.SECRET_KEY
    }
    return headers