import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Products

from api.serializers import ProductsSerializer, ProductDetailSerializer

PRODUCTS_URL = reverse("api:products-list")


def image_upload_url(product_id):
    """Return Url for recipe image upload"""
    return reverse("api:products-upload-image", args=[product_id])


def detail_url(product_id):
    """Return product detail Url"""
    return reverse("api:products-detail", args=[product_id])


@pytest.mark.django_db
def test_auth_required(api_client):  # pylint: disable=unused-argument
    """Test that authentication is required"""
    client = APIClient()
    res = client.get(PRODUCTS_URL)
    assert res.status_code, status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_products(api_client, sample_category, sample_product):
    """Test retrieving a list of Products"""

    client, user = api_client

    product = sample_product(user=user)
    category = sample_category(user=user)
    product.category.add(category)

    res = client.get(PRODUCTS_URL)

    products = Products.objects.all().order_by("-id")
    serializer = ProductsSerializer(products, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


@pytest.mark.django_db
def test_products_limited_to_user(api_client, sample_user, sample_product):
    """Test that the list of products are limited to the user"""
    client, user = api_client

    user2 = sample_user(email="other@bodegonasusalud.com", password="otherpass123")

    sample_product(user=user)
    sample_product(user=user2, name="Ron Cacique")

    res = client.get(PRODUCTS_URL)

    products = Products.objects.filter(user=user)
    serializer = ProductsSerializer(products, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data == serializer.data


@pytest.mark.django_db
def test_view_product_detail(api_client, sample_product, sample_category):
    """Test viewing a product detail"""

    client, user = api_client

    product = sample_product(user=user)
    product.category.add(sample_category(user=user))

    url = detail_url(product.id)
    res = client.get(url)

    serializer = ProductDetailSerializer(product)

    assert res.data == serializer.data
