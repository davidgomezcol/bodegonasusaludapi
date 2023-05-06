from rest_framework import serializers
from django.conf import settings
from typing import Union

from core.models import Categories, Products, Orders, OrderItem


def _product_image_url(filename: object):
    if settings.DEBUG:
        return f"http://localhost/media/{filename}"
    else:
        return f"https://{settings.ALLOWED_HOSTS[0]}/media/{filename}"


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for categories object"""

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductsSerializer(serializers.ModelSerializer):
    """Serializer for products object"""

    category = serializers.StringRelatedField(many=True)
    image = serializers.SerializerMethodField()

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('id', 'category', 'image')

    def get_image(self, obj: Products) -> Union[str, None]:
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
        model = OrderItem
        fields = '__all__'
        read_only_fields = ('id',)


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the orders object"""
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Orders
        fields = '__all__'
        read_only_fields = ('id',)
