import pytest
from django.contrib.auth import get_user_model
from typing import Callable


@pytest.fixture
def sample_user(db) -> Callable[..., get_user_model]:
    def create_sample_user(**kwargs) -> get_user_model:
        return get_user_model().objects.create_user(
            kwargs.get("email", "user@bodegonasusalud.com"),
            kwargs.get("password", "password123"),
        )

    return create_sample_user


@pytest.fixture
def default_sample_user(sample_user: Callable[..., get_user_model]) -> get_user_model:
    return sample_user()


@pytest.fixture
def sample_admin_user(db) -> Callable[..., get_user_model]:
    def create_sample_admin_user(
        email="admin@bodegonasusalud.com", password="password123"
    ) -> get_user_model:
        return get_user_model().objects.create_superuser(email=email, password=password)

    return create_sample_admin_user
