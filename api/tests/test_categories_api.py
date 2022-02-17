from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Categories
from api.serializers import CategoriesSerializer

CATEGORIES_URL = reverse('api:categories-list')


class PublicCategoriesApiTests(TestCase):
    """Test the publicly available categories Api"""
    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving categories"""
        res = self.client.get(CATEGORIES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateCategoriesApiTests(TestCase):
    """Test that authorized user retrieves data from categories Api"""
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'user@bodegonasusalud.com',
            'password123'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_categories(self):
        """Test retrieving categories"""
        Categories.objects.create(user=self.user, name="Vinos")
        Categories.objects.create(user=self.user, name="Rones")

        res = self.client.get(CATEGORIES_URL)

        categories = Categories.objects.all().order_by('-name')
        serializer = CategoriesSerializer(categories, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
