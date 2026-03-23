import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def sample_activity_name():
    return "Chess Club"


@pytest.fixture
def sample_email():
    return "test@mergington.edu"