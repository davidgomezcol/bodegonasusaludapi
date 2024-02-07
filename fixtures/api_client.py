import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client(default_sample_user):
    """Return an authenticated API client."""
    client = APIClient()
    client.force_authenticate(default_sample_user)
    return client, default_sample_user


@pytest.fixture
def custom_api_client(sample_user):
    """Return an authenticated API client."""

    def create_api_client(**kwargs):
        client = APIClient()
        user = kwargs.get("user") or sample_user()
        client.force_authenticate(user)
        return {"client": client, "user": user}

    return create_api_client
