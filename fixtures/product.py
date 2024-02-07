from typing import Optional, Callable

import pytest
from django.contrib.auth import get_user_model

from core.models import Categories, Products

products_info = {
    "name": "Santa Ana",
    "description": "El vino Santa ana es un vino tinto...",
    "price": 15.00,
    "weight": "0.70",
    "units": "l",
    "featured": False,
}


@pytest.fixture
def sample_category(
    sample_user: Callable[..., get_user_model]
) -> Callable[..., Categories]:
    """Create and return a sample category."""

    def create_sample_category(**kwargs) -> Categories:
        user = kwargs.get("user") or sample_user()
        return Categories.objects.create(user=user, name=kwargs.get("name", "Vinos"))

    return create_sample_category


# pylint: disable=unused-argument, redefined-outer-name
@pytest.fixture
def sample_product(
    sample_user: Callable[..., get_user_model],
    sample_category: Callable[..., sample_category],
) -> Callable[..., Products]:
    """Create and return a sample product."""

    def create_sample_product(
        user: Optional[get_user_model] = None,
        category: Optional[Categories] = None,  # pylint: disable=unused-argument
        **kwargs
    ):
        if user is None:
            user = sample_user(**kwargs)
        return Products.objects.create(
            user=user,
            name=kwargs.get("name", products_info["name"]),
            description=kwargs.get("description", products_info["description"]),
            price=kwargs.get("price", products_info["price"]),
            weight=kwargs.get("weight", products_info["weight"]),
            units=kwargs.get("units", products_info["units"]),
            featured=kwargs.get("featured", products_info["featured"]),
        )

    return create_sample_product
