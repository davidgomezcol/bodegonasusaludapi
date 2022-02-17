from rest_framework import serializers

from core.models import Categories


class CategoriesSerializer(serializers.ModelSerializer):
    """Serializer for categories object"""

    class Meta:
        model = Categories
        fields = ('id', 'name')
        read_only_fields = ('id',)
