import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Fixture to get APIClient."""
    return APIClient
