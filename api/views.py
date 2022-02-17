from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Categories
from api import serializers


class CategoriesViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Categories in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Categories.objects.all()
    serializer_class = serializers.CategoriesSerializer
