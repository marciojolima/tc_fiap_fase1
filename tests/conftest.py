from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from api_books_tc.main import app


@pytest.fixture
def client():
    return TestClient(app)
