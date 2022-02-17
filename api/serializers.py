from rest_framework import serializers

from core.models import Categories, Products


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for categories object"""

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id',)


class ProductsSerializer(serializers.ModelSerializer):
    """Serializer for products object"""

    category = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Categories.objects.all()
    )

    class Meta:
        model = Products
        fields = '__all__'
        read_only_fields = ('id',)


class ProductDetailSerializer(ProductsSerializer):
    """Serializer for product details"""
    products = ProductsSerializer(many=True, read_only=True)
    category = CategoriesSerializer(many=True, read_only=True)
