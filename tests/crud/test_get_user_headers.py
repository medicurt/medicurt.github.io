from fastapi.testclient import TestClient
from typing import Dict
from tests.utils.utils import get_user_headers

def test_user_headers(client: TestClient) -> None:
    my_headers = get_user_headers(client)
    assert my_headers != None