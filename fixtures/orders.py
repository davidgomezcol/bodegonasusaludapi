import pytest
from core.models import Orders, OrderItem


@pytest.fixture
def sample_order():
    """Create and return a custom order"""

    def create_sample_order(user, **kwargs):
        defaults = {
            "payment_mode": "Credit Card",
        }
        defaults.update(kwargs)
        return Orders.objects.create(user=user, **defaults)

    return create_sample_order


@pytest.fixture
def sample_order_item():
    """Create and return a sample order item"""

    def create_sample_order_item(
        order, product, quantity, discount, item_price, total_price
    ):  # pylint: disable=too-many-arguments
        return OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            discount=discount,
            item_price=item_price,
            total_price=total_price,
        )

    return create_sample_order_item
