from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Products, Orders, OrderItem

from api.serializers import OrderSerializer

from api.views import OrderViewSet

ORDERS_URL = reverse('api:orders-list')


def create_sample_user():
    """Creates a sample user for tests"""
    return get_user_model().objects.create_user(
        email='user@bodegonasusalud.com', password='password123'
    )


def sample_order(user, **params):
    """Create and return a custom order"""
    defaults = {
        'payment_mode': 'Credit Card',
    }
    defaults.update(params)

    return Orders.objects.create(user=user, **defaults)


def sample_product(user, **params):
    """Create and return a custom product"""
    defaults = {
        'name': 'Ron Cacique',
        'description': 'El ron cacique es...',
        'price': 20,
        'weight': '0.70',
        'units': 'l',
        'featured': True,
    }
    defaults.update(params)

    return Products.objects.create(user=user, **defaults)


def detail_orders_url(order_id):
    """Return orders detail Url"""
    return reverse('api:orders-detail', args=[order_id])


def detail_order_item_url(order_id):
    """Returns Order Item Url"""
    return reverse('api:orderitem-detail', args=[order_id])


class PublicOrdersApiTests(TestCase):
    """Tests that the api is for authenticated users only"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that the authentication is required"""
        res = self.client.get(ORDERS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOrdersApiTests(TestCase):
    """Test authenticated Orders Api Access"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_sample_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_orders(self):
        """Test retrieving a list of Orders"""
        order = sample_order(user=self.user)
        sample_product(user=self.user)

        item = {
            'product': 1,
            'quantity': 2,
        }

        product_selected = Products.objects.get(id=item['product'])

        total_price = OrderViewSet._calculate_total(
            product_selected.price, item['quantity']
        )

        OrderItem.objects.create(
            order=order,
            product=product_selected,
            quantity=item['quantity'],
            discount=product_selected.discount,
            total_price=total_price
        )

        res = self.client.get(ORDERS_URL)

        orders = Orders.objects.all().order_by('-id')
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(len(res.data[0]['order_items']), 1)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_orders_limited_to_user(self):
        """Test that the list of orders are limited to the user"""
        user2 = get_user_model().objects.create_user(
            'other@bodegonasusalud.com',
            'otherpass123'
        )

        sample_order(user=self.user)
        sample_order(user=user2)

        res = self.client.get(ORDERS_URL)

        orders = Orders.objects.filter(user=self.user)
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_order_detail(self):
        """Test viewing an order detail"""
        order = sample_order(user=self.user)
        sample_product(user=self.user)

        item = {
            'product': 1,
            'quantity': 2,
        }

        product_selected = Products.objects.get(id=item['product'])

        total_price = OrderViewSet._calculate_total(
            product_selected.price, item['quantity']
        )

        OrderItem.objects.create(
            order=order,
            product=product_selected,
            quantity=item['quantity'],
            discount=product_selected.discount,
            total_price=total_price
        )

        url = detail_orders_url(order.id)
        res = self.client.get(url)

        serializer = OrderSerializer(order)

        self.assertEqual(len(res.data['order_items']), 1)
        self.assertEqual(res.data, serializer.data)

    def test_view_order_items_detail(self):
        """test viewing an order items detail"""
        sample_product(user=self.user)
        product2 = {
            'user': self.user,
            'name': "Vodka Gordon's",
            'description': "'El Vodka Gordon's es...'",
            'price': 15,
            'weight': '0.70',
            'units': 'l',
            'featured': False,
        }

        Products.objects.create(**product2)

        items = {
            "payment_mode": "Credit Card",
            "order_items": [
                {
                    'product': 1,
                    'quantity': 2,
                },
            ]
        }

        response = self.client.post(
            '/api/orders/',
            items,
            format='json'
        )

        url = detail_order_item_url(1)
        res = self.client.get(url)
        self.assertEqual(len(res.data), 6)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
