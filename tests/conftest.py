from typing import Generator
import pytest
from fastapi.testclient import TestClient


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