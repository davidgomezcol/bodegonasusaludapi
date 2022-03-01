from rest_framework import serializers

from core.models import Categories, Products, Orders, OrderItem


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for categories object"""

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductsSerializer(serializers.ModelSerializer):
    """Serializer for products object"""

    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('id', 'category')


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
