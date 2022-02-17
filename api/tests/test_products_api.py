from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Products, Categories

from api.serializers import CategoriesSerializer, \
    ProductsSerializer, ProductDetailSerializer

PRODUCTS_URL = reverse('api:products-list')


def create_sample_user():
    """Creates a sample user for tests"""
    return get_user_model().objects.create_user(
        email='user@bodegonasusalud.com', password='password123'
    )


def image_upload_url(product_id):
    """Return Url for recipe image upload"""
    return reverse('api:products-upload-image', args=[product_id])


def detail_url(product_id):
    """Return product detail Url"""
    return reverse('api:products-detail', args=[product_id])


def sample_product(user, **params):
    """Create and return a custom product"""
    defaults = {
        'name': 'Ron Cacique',
        'description': 'El ron cacique es...',
        'price': 15,
        'weight': '0.70',
        'units': 'l',
        'featured': True,
    }
    defaults.update(params)

    return Products.objects.create(user=user, **defaults)


def sample_category(user, name="Rones"):
    """Create and return a custom category"""
    return Categories.objects.create(user=user, name=name)


class PublicProductsApiTests(TestCase):
    """Test unauthenticated Products Api access"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required"""
        res = self.client.get(PRODUCTS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProductsApiTests(TestCase):
    """Test authenticated Products Api Access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_products(self):
        """Test retrieving a list of Products"""
        sample_product(user=self.user)
        sample_category(user=self.user)

        res = self.client.get(PRODUCTS_URL)

        products = Products.objects.all().order_by('-id')
        serializer = ProductsSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_products_limited_to_user(self):
        """Test that the list of products are limited to the user"""
        user2 = get_user_model().objects.create_user(
            'other@bodegonasusalud.com',
            'otherpass123'
        )

        sample_product(user=self.user)
        sample_product(user=user2)

        res = self.client.get(PRODUCTS_URL)

        products = Products.objects.filter(user=self.user)
        serializer = ProductsSerializer(products, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_product_detail(self):
        """Test viewing a product detail"""
        product = sample_product(user=self.user)
        product.category.add(sample_category(user=self.user))

        url = detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)
