from typing import Generator, Dict
import pytest
from fastapi.testclient import TestClient
from tests.utils.utils import get_user_headers

from app.core.config import settings
from app.db.session import SessionLocal
from app.main import app


@pytest.fixture(scope="session")
def db() -> Generator:
    yield SessionLocal()

@pytest.fixture(scope="module")
def client()-> Generator:
    with TestClient(app) as c:
        yield c

@pytest.fixture(scope="module")
def user_id() -> int:
    return settings.PYTEST_USER_ID

@pytest.fixture(scope="module")
def user_headers(client: TestClient) -> Dict[str, str]:
    return get_user_headers(client)