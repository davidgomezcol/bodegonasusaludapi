import pytest

from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from core.models import Products, Orders, OrderItem

from api.serializers import OrderSerializer

from api.views import OrderViewSet

ORDERS_URL = reverse("api:orders-list")


def detail_orders_url(order_id):
    """Return orders detail Url"""
    return reverse("api:orders-detail", args=[order_id])


def detail_order_item_url(order_id):
    """Returns Order Item Url"""
    return reverse("api:orderitem-detail", args=[order_id])


@pytest.mark.django_db
def test_auth_required():
    """Test that the authentication is required"""
    client = APIClient()
    res = client.get(ORDERS_URL)
    assert res.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_retrieve_orders(api_client, sample_product, sample_order):
    """Test retrieving a list of Orders"""

    client, user = api_client

    item = {
        "product": 1,
        "quantity": 2,
    }

    sample_product(user=user)

    product_selected = Products.objects.get(id=item["product"])

    total_price = OrderViewSet._calculate_total(
        product_selected.price, item["quantity"]
    )

    sample_order(user=user)

    OrderItem.objects.create(
        order=Orders.objects.get(id=1),
        product=product_selected,
        quantity=item["quantity"],
        discount=product_selected.discount,
        total_price=total_price,
    )

    res = client.get(ORDERS_URL)

    orders = Orders.objects.all().order_by("-id")
    serializer = OrderSerializer(orders, many=True)

    assert len(res.data[0]["order_items"]) == 1
    assert res.status_code == status.HTTP_200_OK
    assert res.data == serializer.data


@pytest.mark.django_db
def test_orders_limited_to_user(custom_api_client, sample_user, sample_order):
    """Test that the list of orders are limited to the user"""

    user2 = sample_user(email="user2@bodegonasusalud.com", password="otherpass123")

    api_data = custom_api_client(user=user2)
    client = api_data["client"]
    user = api_data["user"]

    sample_order(user=user2)

    res = client.get(ORDERS_URL)

    orders = Orders.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)

    assert res.status_code == status.HTTP_200_OK
    assert len(res.data) == 1
    assert res.data == serializer.data


@pytest.mark.django_db
def test_view_order_detail(api_client, sample_product, sample_order, sample_order_item):
    """Test viewing an order detail"""

    client, user = api_client

    sample_product(user=user)

    product_selected = Products.objects.get(name="Santa Ana")

    total_price = OrderViewSet._calculate_total(product_selected.price, 2)

    order = sample_order(user=user)

    sample_order_item(
        order, product_selected, 2, product_selected.discount, total_price
    )

    url = detail_orders_url(order.id)
    res = client.get(url)

    serializer = OrderSerializer(Orders.objects.get(id=order.id))

    assert len(res.data["order_items"]) == 1
    assert res.data == serializer.data


@pytest.mark.django_db
def test_view_order_items_detail(api_client, sample_product):
    """test viewing an order items detail"""

    client, user = api_client

    product = sample_product(user=user)

    items = {
        "payment_mode": "Credit Card",
        "order_items": [
            {
                "product": product.id,
                "quantity": 2,
            },
        ],
    }

    response = client.post("/api/orders/", items, format="json")

    order = Orders.objects.filter(user=user).first()

    latest_order_item = OrderItem.objects.filter(order=order).first()
    order_item_id = latest_order_item.id

    url = detail_order_item_url(order_item_id)
    res = client.get(url)
    assert len(res.data) == 6
    assert res.status_code == status.HTTP_200_OK
    assert response.status_code == status.HTTP_201_CREATED
