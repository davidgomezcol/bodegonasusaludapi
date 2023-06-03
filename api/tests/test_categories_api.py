import pytest

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Categories
from api.serializers import CategoriesSerializer

CATEGORIES_URL = reverse("api:categories-list")


@pytest.mark.django_db
def test_login_required():
    """Test that login is required for retrieving categories"""
    client = APIClient()
    res = client.get(CATEGORIES_URL)

    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_categories(api_client, sample_category):
    """Test retrieving categories"""

    client, user = api_client

    sample_category(user=user, name="Rones")

    res = client.get(CATEGORIES_URL)

    categories = Categories.objects.all().order_by("-name")
    serializer = CategoriesSerializer(categories, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data
