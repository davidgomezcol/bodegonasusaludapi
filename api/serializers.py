from typing import Union

from django.conf import settings
from rest_framework import serializers

from core.models import Categories, Products, Orders, OrderItem


def _product_image_url(filename: object):
    if settings.DEBUG:
        return f"http://localhost/media/{filename}"
    return f"https://{settings.ALLOWED_HOSTS[0]}/media/{filename}"


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for categories object"""

    class Meta:
        """Meta class for categories serializer"""

        model = Categories
        fields = ("id", "name")
        read_only_fields = ("id",)


class ProductsSerializer(serializers.ModelSerializer):
    """Serializer for products object"""

    category = serializers.StringRelatedField(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        """Meta class for products serializer"""

        model = Products
        fields = "__all__"
        read_only_fields = ("id", "category", "image")

    def get_image(self, obj: Products) -> Union[str, None]:
        """Return the image url for the product"""
        if obj.image:
            return _product_image_url(obj.image)
        return None


class ProductDetailSerializer(ProductsSerializer):
    """Serializer for product details"""

    products = ProductsSerializer(many=True, read_only=True)
    category = CategoriesSerializer(many=True, read_only=True)


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the orders items object"""

    class Meta:
        """Meta class for order items serializer"""

        model = OrderItem
        fields = "__all__"
        read_only_fields = ("id",)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the orders object"""

    order_items = OrderItemSerializer(many=True)

    class Meta:
        """Meta class for orders serializer"""

        model = Orders
        fields = "__all__"
        read_only_fields = ("id",)
